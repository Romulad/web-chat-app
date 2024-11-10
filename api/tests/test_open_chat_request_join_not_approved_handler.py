import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect

from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.utils.functions import get_chat_users_from_redis_or_none
from ..app.chat_tools.open_chat_manager import open_chat_manager


class TestOpenChatRequestJoinNotApprovedHandler(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.request_not_approved

    def test_request_not_approved(self, client: TestClient, redis_c):
        chat_id, owner_id = self.create_new_open_chat(client)
        guess_user_id = "user-guess-id"
        connect_to_chat_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.open_chat_add,
            user_id=owner_id,
            user_name="owner"
        )
        request_join_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.request_join,
            user_id=guess_user_id,
            user_name="guess"
        )
        request_join_not_appr_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.request_not_approved,
            user_id=guess_user_id,
            user_name="guess",
            owner_id=owner_id
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{owner_id}") as admin_ws:
            admin_ws.send_json(connect_to_chat_data.model_dump())
            admin_ws.receive_json()

            with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
                guess_ws.send_json(request_join_data.model_dump())
                guess_ws.receive_json()
                admin_ws.receive_json() # admin receive the request to join msg
                
                assert len(open_chat_manager.user_request_sockets.get(chat_id)) == 1

                # sent a no approved msg
                admin_ws.send_json(request_join_not_appr_data.model_dump())
                not_approved_data = guess_ws.receive_json()
                assert not_approved_data.get('chat_id')
                assert not_approved_data.get('type') == open_chat_msg_type.request_not_approved

        assert len(get_chat_users_from_redis_or_none(redis_c, chat_id)) == 1
    

    def test_request_not_approved_send_by_no_admin(self, client: TestClient):
        chat_id, _ = self.create_new_open_chat(client)
        guess_user_id = "user-guess-id"
        request_join_not_appr_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.request_not_approved,
            user_id=guess_user_id,
            user_name="guess",
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
            guess_ws.send_json(request_join_not_appr_data.model_dump())
            data = guess_ws.receive_json()
            assert data.get('type') == open_chat_msg_type.not_allowed_user