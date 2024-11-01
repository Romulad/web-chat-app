import datetime

from fastapi import HTTPException, status, WebSocket

from ..req_resp_models import OpenChatInitSchema, OpenChatMsgDataSchema
from ..utils.constants import open_chat_msg_type
from ..schemas import OpenChatUser, OpenChatRequestJoin
from .open_chat_utils import OpenChatUtils


class OpenChatManager(OpenChatUtils):
    chat_user_sockets: dict[str, dict[str, list[WebSocket]]]
    user_request_sockets: dict[str, list[WebSocket]]
    
    chats : dict[str, list[OpenChatUser]] = {}
    user_requests: list[OpenChatRequestJoin] = []
    chat_owners_ref : dict[str, OpenChatUser] = {}
    chat_msgs: dict = {}

    async def delete_chat(self, chat_id:str):
        if (chat_data := self.chats.get(chat_id)):
            del self.chats[chat_id]
            await self.notify_chat_deletion(chat_id, chat_data)
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Chat can't be found"
            )


    async def on_new_message(self, websocket: WebSocket):
        data = await websocket.receive_json()
        parsed_data = OpenChatMsgDataSchema(**data)
        
        if parsed_data.type == open_chat_msg_type.open_chat_add:
            await self.manage_add_user_to_chat(parsed_data, websocket)
        elif parsed_data.type == open_chat_msg_type.request_join:
            await self.manage_user_request(parsed_data, websocket)
        elif parsed_data.type == open_chat_msg_type.request_approved:
            await self.manage_approved_user_request(parsed_data, websocket)
        elif parsed_data.type == open_chat_msg_type.request_not_approved:
            await self.manage_not_approved_user_request(parsed_data, websocket)
        elif parsed_data.type == open_chat_msg_type.new_message:
            await self.manage_incomming_msg(parsed_data, websocket)
    

    async def manage_add_user_to_chat(
            self, 
            data: OpenChatMsgDataSchema,
            websocket: WebSocket = None,
            existing_websockets: list[WebSocket]=None
    ):
        if (
            chat_data := await self.get_chat_data_or_msg_error(data.chat_id, self.chats, websocket)
        ) == None:
            return

        if(
            user_data := await self.get_user_data_or_msg_error(
                chat_data, data.user_id, websocket
            )
        ) == None:
            return
        
        chat_data.remove(user_data)
        old_websockets = user_data.websockets
        is_already_in_chat = len(user_data.websockets) > 0

        if not existing_websockets:
            old_websockets.append(websocket)
        else:
            old_websockets.extend(existing_websockets)

        user_data.websockets = old_websockets
        chat_data.append(user_data)
        self.chats[data.chat_id] = chat_data
        
        user_list = [
            chat_user.model_dump(exclude={"websockets"}) for chat_user in chat_data
        ]
        connected_user_list = [
            chat_user.model_dump(exclude={"websockets"}) 
            for chat_user in chat_data if chat_user.websockets
        ]

        add_to_chat_data = {
            "type": open_chat_msg_type.added_to_open_chat,
            "chat_id": data.chat_id,
            "chat_users": user_list,
            "connected_users": connected_user_list,
            "chat_msgs": data.data,
        }
        if not existing_websockets:
            await websocket.send_json(add_to_chat_data)
        else:
            await self.broadcast_msg(existing_websockets, add_to_chat_data)

        if not is_already_in_chat:
            await self.broadcast_msg_on_new_user_add(
                data, user_list, connected_user_list,
                [websocket for user_data in chat_data for websocket in user_data.websockets if user_data.user_id != data.user_id]
            )
    

    async def manage_user_request(
            self,
            data: OpenChatMsgDataSchema,
            websocket: WebSocket
    ):        
        if (
            chat_data := await self.get_chat_data_or_msg_error(data.chat_id, self.chats, websocket)
        ) == None:
            return
        
        owner_sockets: list[WebSocket] = []
        for chat_user in chat_data:
            if chat_user.is_owner and chat_user.websockets:
                for owner_websocket in chat_user.websockets:
                   owner_sockets.append(owner_websocket) 
                break
        
        if not owner_sockets:
            data = {
                'chat_id': data.chat_id, 
                "type": open_chat_msg_type.admin_not_conneceted,
                "msg": "Chat admin not connected"
            }
            await websocket.send_json(data)
            return
        
        user_request = self.get_user_request_or_none(self.user_requests, data)

        if user_request:
            self.user_requests.remove(user_request)
            websockets = user_request.websockets
            websockets.append(websocket)
            user_request.websockets = websockets
            self.user_requests.append(user_request)
        else:
            new_user_request = OpenChatRequestJoin(
                chat_id=data.chat_id,
                user_id=data.user_id,
                user_name=data.user_name,
                websockets=[websocket]
            )
            self.user_requests.append(new_user_request)

        request_join_data = {
            "type": open_chat_msg_type.request_join,
            "chat_id": data.chat_id,
            "user_id": data.user_id,
            "user_name": data.user_name,
        }
        request_sent_data = {
            "type": open_chat_msg_type.request_join_sent,
            "chat_id": data.chat_id,
            "msg": (
                f"Request to join sent for {data.chat_id}" 
                if not user_request 
                else f"Request to join sent for {data.chat_id} again"
            )
        }
        await self.broadcast_msg(owner_sockets, request_join_data)
        await websocket.send_json(request_sent_data)


    async def manage_approved_user_request(
            self, 
            data: OpenChatMsgDataSchema,
            websocket: WebSocket
    ):
        user_request = self.get_user_request_or_none(self.user_requests, data)
        if not user_request:
            await websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User request can't be found anymore; for ${data.user_name}",
                    "chat_id": data.chat_id,
                    "user_id": data.user_id
                }
            )
            return
    
        self.user_requests.remove(user_request)

        if not user_request.websockets:
            await websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User request was approved but ${data.user_name} is not connected anymore",
                    "chat_id": data.chat_id,
                    "user_id": data.user_id
                }
            )
            return

        request_approved_data = {
            "type": open_chat_msg_type.request_approved,
            "chat_id": data.chat_id,
        }
        await self.broadcast_msg(user_request.websockets, request_approved_data)
        await self.add_to_chat_on_approved_request(user_request, data.data)


    async def add_to_chat_on_approved_request(self, user_request: OpenChatRequestJoin, chat_msgs):
        new_data = OpenChatMsgDataSchema(
            user_name=user_request.user_name,
            chat_id=user_request.chat_id,
            data=chat_msgs,
            type="",
            user_id=user_request.user_id
        )
        await self.manage_add_user_to_chat(new_data, existing_websockets=user_request.websockets)
        
    
    async def manage_not_approved_user_request(
            self, 
            data: OpenChatMsgDataSchema,
            websocket: WebSocket
    ):
        user_request = self.get_user_request_or_none(self.user_requests, data)

        if not user_request:
            return
        
        self.user_requests.remove(user_request)
        
        if not user_request.websockets:
            await websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User request rejected; but ${data.user_name} is not connected anymore",
                    "chat_id": data.chat_id,
                    "user_id": data.user_id
                }
            )
            return

        request_not_approved_data = {
            "type": open_chat_msg_type.request_not_approved,
            "chat_id": data.chat_id,
        }
        await self.broadcast_msg(user_request.websockets, request_not_approved_data)


    async def broadcast_msg_on_new_user_add(
            self, data: OpenChatMsgDataSchema, 
            user_list: list,
            connected_users: list,
            websockets: list[WebSocket]
    ):
        broadcast_data = {
            "type": open_chat_msg_type.notify_new_user,
            "chat_id": data.chat_id,
            "user_name": data.user_name,
            "user_id": data.user_id,
            "chat_users": user_list,
            "connected_users": connected_users
        }
        await self.broadcast_msg(websockets, broadcast_data)
    

    async def manage_incomming_msg(
        self,
        data: OpenChatMsgDataSchema,
        websocket: WebSocket
    ):
        if (
            chat_data := await self.get_chat_data_or_msg_error(data.chat_id, self.chats, websocket)
        ) == None:
            return
        
        resp_data = OpenChatMsgDataSchema(
            chat_id=data.chat_id,
            data=data.data,
            type=open_chat_msg_type.new_message,
            user_id=data.user_id,
            user_name=data.user_name
        ) 
        await self.broadcast_msg(
            [websocket for chat_user in chat_data for websocket in chat_user.websockets if chat_user.user_id != data.user_id],
            resp_data.model_dump(),
        )
    

    async def notify_chat_deletion(self, chat_id: str, chat_data: list[OpenChatUser]):
        resp_data = {
            "chat_id": chat_id,
            "type": open_chat_msg_type.chat_deleted
        }
        await self.broadcast_msg(
            [websocket for chat_user in chat_data for websocket in chat_user.websockets],
            resp_data
        )
    

    async def disconnect_user(
        self, websocket: WebSocket, chat_id: str, user_id: str
    ):
        await self.manage_chat_disconnection(websocket, chat_id, user_id)
        self.manage_user_request_deletion(websocket, chat_id, user_id)
        

    def manage_user_request_deletion(
        self, websocket: WebSocket, chat_id: str, user_id: str
    ):
        for user_request in self.user_requests:
            if (
                user_request.chat_id == chat_id and 
                user_request.user_id == user_id
            ):
                try:
                    user_request.websockets.remove(websocket)
                except ValueError:
                    pass
            
                if not user_request.websockets:
                    try:
                        self.user_requests.remove(user_request)
                    except ValueError:
                        pass
                break


    async def manage_chat_disconnection(
        self, websocket: WebSocket, chat_id: str, user_id: str
    ):
        chat_user = self.get_user_data_or_none(self.chats, chat_id, user_id)
        if not chat_user:
            return
        
        try:
            chat_user.websockets.remove(websocket)
        except ValueError:
            pass

        if not chat_user.websockets:
            data = {
                "chat_id": chat_id,
                "user_id": user_id,
                "user_name": chat_user.name,
                "type": open_chat_msg_type.user_disconnect
            }
            chat_data = self.chats.get(chat_id, [])
            await self.broadcast_msg(
                [websocket for user in chat_data for websocket in user.websockets if user.user_id != user_id], 
                data
            )
            
        

open_chat_manager = OpenChatManager()