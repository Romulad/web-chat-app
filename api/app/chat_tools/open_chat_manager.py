import datetime

from fastapi import WebSocket

from ..req_resp_models import OpenChatMsgDataSchema
from ..utils.constants import open_chat_msg_type
from ..schemas import OpenChatUser, OpenChatMsg
from .open_chat_utils import OpenChatUtils
from ..utils.functions import (
    get_chat_msgs_from_redis_or_none, 
    get_redis_from_request,
    get_owner_data_from_redis_or_none,
    stringify,
    get_chat_users_from_redis_or_none
)
from ..redis import redis_key


class OpenChatManager(OpenChatUtils):
    chat_user_sockets: dict[str, dict[str, list[WebSocket]]] = {}
    user_request_sockets: dict[str, dict[str, list[WebSocket]]] = {}

    async def on_new_message(self, websocket: WebSocket):
        data = await websocket.receive_json()
        parsed_data = OpenChatMsgDataSchema(**data)

        if (
            await self.get_chat_data_or_msg_error(parsed_data.chat_id, websocket)
        ) == None:
            return
        
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
        redis_c = get_redis_from_request(websocket if websocket else existing_websockets[0])
        chat_data = get_chat_users_from_redis_or_none(redis_c, data.chat_id)
        owner_data = get_owner_data_from_redis_or_none(redis_c, data.chat_id)
        
        # check if user is a chat user first
        if(
            user_data := await self.get_user_data_or_msg_error(
                chat_data, data.user_id, websocket
            )
        ) == None:
            return
        
        # update active user chat connections
        chat_users_conn = self.chat_user_sockets.get(data.chat_id, {})
        user_conn = chat_users_conn.get(data.user_id, [])
        user_conn.extend(existing_websockets) if existing_websockets else user_conn.append(websocket)
        chat_users_conn[data.user_id] = user_conn
        self.chat_user_sockets[data.chat_id] = chat_users_conn
        
        connected_user_ids = [
            user_conn_id for user_conn_id, _ in chat_users_conn.items()
        ]

        add_to_chat_data = {
            "type": open_chat_msg_type.added_to_open_chat,
            "chat_id": data.chat_id,
            "chat_name": owner_data.get('chat_name', ""),
            "created_at": owner_data.get('created_at', ""),
            "chat_users": chat_data,
            "connected_users": connected_user_ids,
            "chat_msgs": get_chat_msgs_from_redis_or_none(
                redis_c, data.chat_id
            ),
        }
        if not existing_websockets:
            await websocket.send_json(add_to_chat_data)
        else:
            await self.broadcast_msg(existing_websockets, add_to_chat_data)

        if (
            (existing_websockets and (len(user_conn) == len(existing_websockets))) or 
            (not existing_websockets and len(user_conn) == 1)
        ):
            await self.broadcast_msg_on_new_user_add(
                data, chat_data, connected_user_ids,
                [
                    websocket for conn_user_id, conns in chat_users_conn.items() 
                    for websocket in conns if user_data.user_id != conn_user_id
                ]
            )


    async def manage_user_request(
            self,
            data: OpenChatMsgDataSchema,
            websocket: WebSocket
    ):        
        redis_c = get_redis_from_request(websocket)
        owner_data = get_owner_data_from_redis_or_none(redis_c, data.chat_id)
        owner_data = OpenChatUser(**owner_data) if owner_data else None
        
        # get owner connections
        chat_connections = self.chat_user_sockets.get(data.chat_id, {})
        owner_sockets: list[WebSocket] = []
        if (
            owner_data and 
            owner_data.is_owner and 
            (owner_connections := chat_connections.get(owner_data.user_id))
        ):
            if owner_connections:
                owner_sockets.extend(owner_connections)
        
        # notify user when chat admin is not connected to approve the request
        if not owner_sockets:
            data = {
                'chat_id': data.chat_id, 
                "type": open_chat_msg_type.admin_not_conneceted,
                "msg": "Chat admin not connected"
            }
            await websocket.send_json(data)
            return

        # Update user request to join connection
        request_connections = self.user_request_sockets.get(data.chat_id, {})
        connections = request_connections.get(data.user_id, [])
        connections.append(websocket)
        request_connections[data.user_id] = connections
        self.user_request_sockets[data.chat_id] = request_connections
        
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
                f"Request to join sent for {data.chat_id} again"
                if len(connections) > 1 else 
                f"Request to join sent for {data.chat_id}" 
            )
        }
        await self.broadcast_msg(owner_sockets, request_join_data)
        await websocket.send_json(request_sent_data)


    async def manage_approved_user_request(
            self, 
            data: OpenChatMsgDataSchema,
            websocket: WebSocket
    ):
        redis_c = get_redis_from_request(websocket)
        chat_users = get_chat_users_from_redis_or_none(redis_c, data.chat_id)
        
        # request should be approved only if it was initiate by an admin
        is_admin = self.is_chat_admin(websocket, data.chat_id, data.owner_id)
        if not is_admin:
            await websocket.send_json({"type": open_chat_msg_type.not_allowed_user})
            return

        chat_request_join = self.user_request_sockets.get(data.chat_id, {})
        user_request_conns = chat_request_join.get(data.user_id)
        if not user_request_conns:
            await websocket.send_json(
                {
                    "type": open_chat_msg_type.notification,
                    "msg": f"User request can't be found anymore; for {data.user_name}",
                    "chat_id": data.chat_id,
                    "user_id": data.user_id
                }
            )
            return

        # clean up request join connection for the user
        del chat_request_join[data.user_id] 
        self.user_request_sockets[data.chat_id] = chat_request_join
        
        chat_users.append(OpenChatUser(
            user_id=data.user_id,
            is_owner=False,
            name=data.user_name,
            created_at=datetime.datetime.now().isoformat()
        ).model_dump())
        redis_c.hset(redis_key.chats, data.chat_id, stringify(chat_users))
    
        request_approved_data = {
            "type": open_chat_msg_type.request_approved,
            "chat_id": data.chat_id,
        }
        await self.broadcast_msg(user_request_conns, request_approved_data)
        await self.add_to_chat_on_approved_request(
            data.chat_id,
            user_request_conns,
            data.user_id,
            data.user_name
        )


    async def add_to_chat_on_approved_request(
            self, 
            chat_id,
            user_websockets: list[WebSocket],
            user_id,
            user_name
    ):
        new_data = OpenChatMsgDataSchema(
            user_name=user_name,
            chat_id=chat_id,
            type="",
            user_id=user_id,
            data="",
        )
        await self.manage_add_user_to_chat(new_data, existing_websockets=user_websockets)
        
    
    async def manage_not_approved_user_request(
            self, 
            data: OpenChatMsgDataSchema,
            websocket: WebSocket
    ):  
        # only the chat admin can declined a request to join
        is_admin = self.is_chat_admin(websocket, data.chat_id, data.owner_id)
        if not is_admin:
            await websocket.send_json({"type": open_chat_msg_type.not_allowed_user})
            return

        chat_request_join = self.user_request_sockets.get(data.chat_id, {})
        user_request_conns = chat_request_join.get(data.user_id)
        if not user_request_conns:
            return

        # clean up request to join connections   
        del chat_request_join[data.user_id] 
        self.user_request_sockets[data.chat_id] = chat_request_join

        request_not_approved_data = {
            "type": open_chat_msg_type.request_not_approved,
            "chat_id": data.chat_id,
        }
        await self.broadcast_msg(user_request_conns, request_not_approved_data)


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
        redis_c = get_redis_from_request(websocket)
        chat_msgs = get_chat_msgs_from_redis_or_none(redis_c, data.chat_id)
        user_exists = self.get_user_data_or_none(websocket, data.chat_id, data.user_id)

        # user should exist in the chat before sending a message
        if not user_exists:
            await websocket.send_json({"type": open_chat_msg_type.not_allowed_user})
            return

        # user can not send empty message
        if not data.data:
            await websocket.send_json({"msg": "No message"})
            return

        # add msg to redis
        msg_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
        msg_data = OpenChatMsg(
            chat_id=data.chat_id,
            send_at=msg_date,
            sender_id=data.user_id,
            sender_name=data.user_name,
            msg=data.data
        )
        chat_msgs.append(msg_data.model_dump())
        redis_c.hset(redis_key.chat_msgs, data.chat_id, stringify(chat_msgs))
        
        chat_conns = self.chat_user_sockets.get(data.chat_id, {})
        resp_data = OpenChatMsgDataSchema(
            chat_id=data.chat_id,
            data=data.data,
            type=open_chat_msg_type.new_message,
            user_id=data.user_id,
            user_name=data.user_name,
            send_at=msg_date
        ) 
        await self.broadcast_msg(
            [websocket for user_id, user_conns in chat_conns.items() for websocket in user_conns if user_id != data.user_id],
            resp_data.model_dump(),
        )

    
    async def manage_chat_deletion(self, chat_id: str, owner_id: str):
        await self.notify_chat_deletion(chat_id, owner_id)
        self.manage_socket_deletion(chat_id)


    async def notify_chat_deletion(self, chat_id: str, owner_id: str):        
        resp_data = {
            "chat_id": chat_id,
            "owner_id": owner_id,
            "type": open_chat_msg_type.chat_deleted
        }
        chat_user_connections = self.chat_user_sockets.get(chat_id, {})
        await self.broadcast_msg(
            [
                websocket 
                for user_id, websockets in chat_user_connections.items() 
                for websocket in websockets if user_id != owner_id
            ],
            resp_data
        )


    def manage_socket_deletion(self, chat_id: str):
        if self.chat_user_sockets.get(chat_id) != None:
            del self.chat_user_sockets[chat_id]
        
        if self.user_request_sockets.get(chat_id) != None:
            del self.user_request_sockets[chat_id]
    

    async def disconnect_websocket(
        self, websocket: WebSocket, chat_id: str, user_id: str
    ):
        await self.delete_user_socket_from_chat(websocket, chat_id, user_id)
        self.delete_user_socket_from_request_join(websocket, chat_id, user_id)
        

    def delete_user_socket_from_request_join(
        self, websocket: WebSocket, chat_id: str, user_id: str
    ):
        chat_requests_join = self.user_request_sockets.get(chat_id, {})
        request_socket_conns = chat_requests_join.get(user_id)

        if request_socket_conns:
            try:
                request_socket_conns.remove(websocket)
            except ValueError:
                pass
        
        if not request_socket_conns:
            try:
                del chat_requests_join[user_id]
            except KeyError:
                pass


    async def delete_user_socket_from_chat(
        self, websocket: WebSocket, chat_id: str, user_id: str
    ):
        chat_user = self.get_user_data_or_none(websocket, chat_id, user_id)
        if not chat_user:
            return
        
        chat_conns = self.chat_user_sockets.get(chat_id, {})
        user_conns = chat_conns.get(user_id, [])
        
        try:
            user_conns.remove(websocket)
        except ValueError:
            pass

        if not user_conns:
            data = {
                "chat_id": chat_id,
                "user_id": user_id,
                "user_name": chat_user.name,
                "type": open_chat_msg_type.user_disconnect
            }
            await self.broadcast_msg(
                [
                    websocket for connec_user_id, conns in chat_conns.items() 
                    for websocket in conns if connec_user_id != user_id
                ], 
                data
            )
            try:
                del chat_conns[user_id]
            except KeyError:
                pass
           

open_chat_manager = OpenChatManager()