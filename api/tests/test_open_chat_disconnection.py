from fastapi.testclient import TestClient

from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.chat_tools.open_chat_manager import open_chat_manager


class TestOpenchatDisconnection(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.open_chat_add

    def test_open_chat_disconnection(self, client: TestClient):
        chat_id, owner_id = self.create_new_open_chat()

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
            assert self.get_open_chat_user_data_or_none(
                chat_id, owner_id
            ).websockets
        
        assert not self.get_open_chat_user_data_or_none(
            chat_id, owner_id
        ).websockets
        assert len(open_chat_manager.chats[chat_id]) == 1

    def test_open_chat_disconnection_with_broadcast(self, client: TestClient):
        chat_id, owner_id = self.create_new_open_chat()
        self.add_user_to_open_chat(chat_id, "guess_id", "guess")

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
            assert self.get_open_chat_user_data_or_none(
                chat_id, owner_id
            ).websockets

            with client.websocket_connect(self.route + chat_id + "/guess_id") as wb1:
                wb1.send_json(user1_msg_data.model_dump())
                wb1.receive_json()
                wb.receive_json() # after new is added to a chat, notification msg
                assert self.get_open_chat_user_data_or_none(
                    chat_id, "guess_id"
                ).websockets

            # broadcast should happen because guess sockets doesn't exist anymore
            broad_cast_msg = wb.receive_json()
            assert broad_cast_msg.get('chat_id')
            assert broad_cast_msg.get('user_id')
            assert broad_cast_msg.get('user_name')
            assert broad_cast_msg.get('type') == open_chat_msg_type.user_disconnect
        
        assert not self.get_open_chat_user_data_or_none(
            chat_id, owner_id
        ).websockets
        assert not self.get_open_chat_user_data_or_none(
            chat_id, "guess_id"
        ).websockets
        assert len(open_chat_manager.chats[chat_id]) == 2
