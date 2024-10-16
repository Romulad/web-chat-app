import datetime
from uuid import uuid1

from fastapi import HTTPException, status, WebSocket

from ..req_resp_models import OpenChatInitSchema, OpenChatMsgDataSchema
from ..utils.constants import open_chat_msg_type
from ..schemas import OpenChatUser, OpenChatRequestJoin


class OpenChatManager:
    chats : dict[str, list[OpenChatUser]] = {}
    user_requests: list[OpenChatRequestJoin] = []
    websocket : WebSocket
    data: OpenChatMsgDataSchema

    def create_new_chat(self, chat_data:OpenChatInitSchema):
        user_data = OpenChatUser(
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            is_owner=True,
            name=chat_data.initiator_name,
            user_id=chat_data.initiator_id
        )
        self.chats[chat_data.chat_id] = [user_data]


    def delete_chat(self, chat_id:str):
        if self.chats.get(chat_id):
            del self.chats[chat_id]
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Chat can't be found"
            )


    async def on_new_message(self, websocket: WebSocket):
        data = await websocket.receive_json()
        parsed_data = OpenChatMsgDataSchema(**data)

        self.websocket = websocket
        self.data = parsed_data

        if parsed_data.type == open_chat_msg_type.open_chat_add:
            await self.manage_add_user_to_chat()
        elif parsed_data.type == open_chat_msg_type.request_join:
            await self.manage_user_request()
        elif parsed_data.type == open_chat_msg_type.request_approved:
            await self.manage_approved_user_request()
        elif parsed_data.type == open_chat_msg_type.request_not_approved:
            await self.manage_not_approved_user_request()


    async def get_chat_data_or_msg_error(self):
        if not (chat_data := self.chats.get(self.data.chat_id)):
            resp_data = {"msg": "Chat not found", "chat_id": self.data.chat_id, "type": open_chat_msg_type.error}
            await self.websocket.send_json(resp_data)
            return
        return chat_data
    

    async def manage_add_user_to_chat(self, existing_websockets: list[WebSocket]=None):
        if not (chat_data := await self.get_chat_data_or_msg_error()):
            return

        user_data = None
        for existing_user in chat_data:
            if existing_user.user_id == self.data.user_id:
                user_data = existing_user
        
        if user_data:
            chat_data.remove(user_data)
            websockets = user_data.websockets

            if not existing_websockets:
                websockets.append(self.websocket)
            else:
                websockets.extend(existing_websockets)

            user_data.websockets = websockets
            chat_data.append(user_data)
            self.chats[self.data.chat_id] = chat_data
        else:
            new_user = OpenChatUser(
                is_owner=False,
                name=self.data.user_name,
                user_id=self.data.user_id,
                websockets=[self.websocket] if not existing_websockets else existing_websockets,
                created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )
            chat_data.append(new_user)
            self.chats[self.data.chat_id] = chat_data
        
        data = {
            "type": open_chat_msg_type.added_to_open_chat,
            "data": {
             "chat_id": self.data.chat_id,
             "users": [chat_user.model_dump(exclude={"websockets"}) for chat_user in chat_data]
            }
        }
        if not existing_websockets:
            await self.websocket.send_json(data)
        else:
            await self.broadcast_msg(existing_websockets, data)

        if not user_data:
            await self.broadcast_msg_on_new_user_add(
                [websocket for user_data in chat_data for websocket in user_data.websockets if user_data.user_id != self.data.user_id]
            )
    

    async def manage_user_request(self):
        if not (chat_data := await self.get_chat_data_or_msg_error()):
            return
        
        owner_sockets: list[WebSocket] = []
        for chat_user in chat_data:
            if chat_user.is_owner and chat_user.websockets:
                for websocket in chat_user.websockets:
                   owner_sockets.append(websocket) 
                break
        
        if not owner_sockets:
            data = {
                'chat_id': self.data.chat_id, 
                "type": open_chat_msg_type.admin_not_conneceted,
                "msg": "Chat admin not connected"
            }
            await self.websocket.send_json(data)
            return
        
        user_request = self.get_user_request_or_none()

        if user_request:
            self.user_requests.remove(user_request)
            websockets = user_request.websockets
            websockets.append(self.websocket)
            user_request.websockets = websockets
            self.user_requests.append(user_request)
        else:
            new_user_request = OpenChatRequestJoin(
                chat_id=self.data.chat_id,
                user_id=self.data.user_id,
                user_name=self.data.user_name,
                websockets=[self.websocket]
            )
            self.user_requests.append(new_user_request)

        request_join_data = {
            "type": open_chat_msg_type.request_join,
            "chat_id": self.data.chat_id,
            "user_id": self.data.user_id,
            "user_name": self.data.user_name,
        }
        request_sent_data = {
            "type": open_chat_msg_type.request_join_sent,
            "chat_id": self.data.chat_id,
            "msg": (
                f"Request to join sent for ${self.data.chat_id}" 
                if not user_request 
                else f"Request to join sent for ${self.data.chat_id} again"
            )
        }
        await self.broadcast_msg(owner_sockets, request_join_data)
        await self.websocket.send_json(request_sent_data)
    

    def get_user_request_or_none(self):
        request = None
        for existing_request in self.user_requests:
            if (
                existing_request.chat_id == self.data.chat_id and 
                existing_request.user_id == self.data.user_id
            ):
                request = existing_request
                break
        
        return request


    async def manage_approved_user_request(self):
        user_request = self.get_user_request_or_none()
        if not user_request:
            await self.websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User request can't be found anymore for ${self.data.user_name}",
                    "chat_id": self.data.chat_id,
                    "user_id": self.data.user_id
                }
            )
            return

        if not user_request.websockets:
            await self.websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User request was approved but ${self.data.user_name} is not connected anymore",
                    "chat_id": self.data.chat_id,
                    "user_id": self.data.user_id
                }
            )
            return

        self.user_requests.remove(user_request)
        request_approved_data = {
            "type": open_chat_msg_type.request_approved,
            "chat_id": self.data.chat_id,
            "owner_name": self.data.data.get('owner_name')
        }
        await self.broadcast_msg(user_request.websockets, request_approved_data)

        new_data = OpenChatMsgDataSchema(
            user_name=user_request.user_name,
            chat_id=user_request.chat_id,
            data="",
            type="",
            user_id=user_request.user_id
        )
        self.data = new_data
        await self.manage_add_user_to_chat(user_request.websockets)
        
    
    async def manage_not_approved_user_request(self):
        user_request = self.get_user_request_or_none()

        if not user_request:
            return
        
        if not user_request.websockets:
            await self.websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User Request rejected: ${self.data.user_name} is no connected",
                    "chat_id": self.data.chat_id,
                    "user_id": self.data.user_id
                }
            )
            return

        self.user_requests.remove(user_request)
        request_not_approved_data = {
            "type": open_chat_msg_type.request_not_approved,
            "chat_id": self.data.chat_id,
            "owner_name": self.data.data.get('owner_name')
        }
        await self.broadcast_msg(user_request.websockets, request_not_approved_data)


    async def broadcast_msg_on_new_user_add(self, websockets: list[WebSocket]):
        broadcast_data = {
            "type": open_chat_msg_type.notify_new_user,
            "data": {
                "chat_id": self.data.chat_id,
                "user_name": self.data.user_name,
                "user_id": self.data.user_id,
            }
        }
        await self.broadcast_msg(websockets, broadcast_data)
    
    async def broadcast_msg(
        self, websockets: list[WebSocket], data: dict
    ):
        for websocket in websockets:
            await websocket.send_json(data)
        


open_chat_manager = OpenChatManager()