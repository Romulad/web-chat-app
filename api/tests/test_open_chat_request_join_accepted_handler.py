from fastapi.testclient import TestClient

from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.utils.functions import get_chat_users_from_redis_or_none


class TestOpenChatRequestJoinApprovedHandler(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.request_approved

    def test_request_approved(self, client: TestClient, redis_c):
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
        request_join_appr_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.request_approved,
            user_id=guess_user_id,
            user_name="guess",
            owner_id=owner_id
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{owner_id}") as admin_ws:
            admin_ws.send_json(connect_to_chat_data.model_dump())
            admin_ws.receive_json()

            # once admin is connected, user request to join
            with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
                guess_ws.send_json(request_join_data.model_dump())
                guess_ws.receive_json()
                admin_ws.receive_json()

                admin_ws.send_json(request_join_appr_data.model_dump())
                approved_data = guess_ws.receive_json()
                assert approved_data.get('type') == open_chat_msg_type.request_approved

                added_data = guess_ws.receive_json()
                assert added_data.get('type') == open_chat_msg_type.added_to_open_chat
                assert added_data.get('chat_id')
                assert added_data.get('chat_users')
                assert len(added_data.get('chat_users')) == 2
                assert added_data.get('connected_users')
                assert len(added_data.get('connected_users')) == 2
                assert isinstance(added_data.get('chat_msgs'), list)

                notify_new_user = admin_ws.receive_json()
                assert notify_new_user.get('type') == open_chat_msg_type.notify_new_user
                assert notify_new_user.get('chat_id')
                assert notify_new_user.get('user_id')
                assert notify_new_user.get('user_name')
                assert len(notify_new_user.get('chat_users')) == 2
                assert len(notify_new_user.get('connected_users')) == 2

        assert len(get_chat_users_from_redis_or_none(redis_c, chat_id)) == 2


    def test_approved_no_existing_request(self, client: TestClient):
        chat_id, owner_id = self.create_new_open_chat(client)
        guess_user_id = "user-guess-id"
        connect_to_chat_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.open_chat_add,
            user_id=owner_id,
            user_name="owner"
        )
        request_join_appr_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.request_approved,
            user_id=guess_user_id,
            user_name="guess",
            owner_id=owner_id
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{owner_id}") as admin_ws:
            admin_ws.send_json(connect_to_chat_data.model_dump())
            admin_ws.receive_json()

            # sent an approved msg but the request to join doesn't exist anymore
            admin_ws.send_json(request_join_appr_data.model_dump())
            request_not_existe_data = admin_ws.receive_json()
            assert request_not_existe_data.get('chat_id')
            assert request_not_existe_data.get('user_id')
            assert request_not_existe_data.get('type') == open_chat_msg_type.notification
            assert request_not_existe_data.get('msg') == f"User request can't be found anymore; for guess"


    def test_request_approved_send_by_no_admin(self, client: TestClient):
        chat_id, _ = self.create_new_open_chat(client)
        guess_user_id = "user-guess-id"
        request_join_appr_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.request_approved,
            user_id=guess_user_id,
            user_name="guess",
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
            guess_ws.send_json(request_join_appr_data.model_dump())
            data = guess_ws.receive_json()
            assert data.get('type') == open_chat_msg_type.not_allowed_user