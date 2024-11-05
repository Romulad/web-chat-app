from redis import Redis
from fastapi.testclient import TestClient

from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.chat_tools.open_chat_manager import open_chat_manager
from ..app.utils.functions import get_chat_users_from_redis_or_none


class TestOpenchatDisconnection(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.open_chat_add

    def test_open_chat_disconnection(self, client: TestClient, redis_c: Redis):
        chat_id, owner_id = self.create_new_open_chat(client)

        owner_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id=owner_id,
            user_name="owner",
        )

        with client.websocket_connect(self.route + chat_id + "/" + owner_id) as wb:
            wb.send_json(owner_msg_data.model_dump())
            wb.receive_json()
            assert open_chat_manager.chat_user_sockets.get(chat_id).get(owner_id)
        
        assert not open_chat_manager.chat_user_sockets.get(chat_id).get(owner_id)
        assert len(get_chat_users_from_redis_or_none(redis_c, chat_id)) == 1

    def test_open_chat_disconnection_with_broadcast(
            self, 
            client: TestClient,
            redis_c
    ):
        chat_id, owner_id = self.create_new_open_chat(client)
        self.add_user_to_open_chat(chat_id, "guess_id", redis_c, "guess")
        user_id = "request_join_user_id"
        req_join_data = self.get_request_join_data(chat_id, user_id)

        owner_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id=owner_id,
            user_name="owner",
        )

        user1_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id="guess_id",
            user_name="guess",
        )



        with client.websocket_connect(self.route + chat_id + "/" + owner_id) as wb:
            wb.send_json(owner_msg_data.model_dump())
            wb.receive_json()
            assert open_chat_manager.chat_user_sockets.get(chat_id).get(owner_id)

            with client.websocket_connect(self.route + chat_id + "/guess_id") as wb1:
                wb1.send_json(user1_msg_data.model_dump())
                wb1.receive_json()
                wb.receive_json() # after new is added to a chat, notification msg
                assert open_chat_manager.chat_user_sockets.get(chat_id).get("guess_id")
            
            # broadcast should happen because guess sockets doesn't exist anymore
            broad_cast_msg = wb.receive_json()
            assert broad_cast_msg.get('chat_id')
            assert broad_cast_msg.get('user_id')
            assert broad_cast_msg.get('user_name')
            assert broad_cast_msg.get('type') == open_chat_msg_type.user_disconnect

            # User request to join with admin connected
            with client.websocket_connect(f"{self.route}{chat_id}/{user_id}") as guess_wb:
                guess_wb.send_json(req_join_data.model_dump())
                guess_wb.receive_json()
                wb.receive_json() # msg for request sent to admin
                assert open_chat_manager.user_request_sockets.get(chat_id).get(user_id)
        
        assert not open_chat_manager.chat_user_sockets.get(chat_id).get(owner_id)
        assert not open_chat_manager.chat_user_sockets.get(chat_id).get("guess_id")
        assert not open_chat_manager.user_request_sockets.get(chat_id).get(user_id)
        assert len(get_chat_users_from_redis_or_none(redis_c, chat_id)) == 2
