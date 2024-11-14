from fastapi.testclient import TestClient

from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.utils.functions import get_chat_msgs_from_redis_or_none


class TestOpenChatMessageHandler(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.new_message

    def test_message_by_not_chat_user(self, client: TestClient, redis_c):
        chat_id, _ = self.create_new_open_chat(client)
        guess_user_id = "guess-my-user-id"

        msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="I want to impact your life",
            type=open_chat_msg_type.new_message,
            user_id=guess_user_id,
            user_name="owner"
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
            guess_ws.send_json(msg_data.model_dump())
            not_allowed_data = guess_ws.receive_json()
            assert not_allowed_data.get('type') == open_chat_msg_type.not_allowed_user
        
        assert len(get_chat_msgs_from_redis_or_none(redis_c, chat_id)) == 0


    def test_with_not_msg_data(self, client: TestClient, redis_c):
        chat_id, _ = self.create_new_open_chat(client)
        guess_user_id = "guess-my-user-id"
        self.add_user_to_open_chat(chat_id, guess_user_id, redis_c)

        msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.new_message,
            user_id=guess_user_id,
            user_name="guess"
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
            guess_ws.send_json(msg_data.model_dump())
            not_allowed_data = guess_ws.receive_json()
            assert "No message" in not_allowed_data.get('msg')
        
        assert len(get_chat_msgs_from_redis_or_none(redis_c, chat_id)) == 0


    def test_message_between_users(self, client: TestClient, redis_c):
        chat_id, owner_id = self.create_new_open_chat(client)
        guess_user_id = "guess-my-user-id"
        self.add_user_to_open_chat(chat_id, guess_user_id, redis_c)

        ask_to_join_admin = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.open_chat_add,
            user_id=owner_id,
            user_name="owner"
        )
        ask_to_join_guess = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.open_chat_add,
            user_id=guess_user_id,
            user_name="guess"
        )

        admin_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="Hi, guess",
            type=open_chat_msg_type.new_message,
            user_id=owner_id,
            user_name="owner"
        )
        guess_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="Yeah, hi what's up",
            type=open_chat_msg_type.new_message,
            user_id=guess_user_id,
            user_name="guess"
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{owner_id}") as admin_ws:
            admin_ws.send_json(ask_to_join_admin.model_dump())
            admin_ws.receive_json()

            with client.websocket_connect(f"{self.route}{chat_id}/{guess_user_id}") as guess_ws:
                guess_ws.send_json(ask_to_join_guess.model_dump())
                guess_ws.receive_json()
                admin_ws.receive_json()

                admin_ws.send_json(admin_msg_data.model_dump())
                admin_msg = guess_ws.receive_json()
                assert admin_msg.get("type") == open_chat_msg_type.new_message
                assert admin_msg.get("chat_id")
                assert admin_msg.get("user_id")
                assert admin_msg.get("user_name")
                assert admin_msg.get("data") == "Hi, guess"

                guess_ws.send_json(guess_msg_data.model_dump())
                guess_msg = admin_ws.receive_json()
                assert guess_msg.get("type") == open_chat_msg_type.new_message
                assert guess_msg.get("chat_id")
                assert guess_msg.get("user_id")
                assert guess_msg.get("user_name")
                assert guess_msg.get("data") == "Yeah, hi what's up"
    
        assert len(get_chat_msgs_from_redis_or_none(redis_c, chat_id)) == 2