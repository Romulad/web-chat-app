from fastapi.testclient import TestClient

from ..app.utils.constants import open_chat_msg_type
from .open_chat_route_common_performed import CommonTest
from .base_classes import BaseOpenChatTestClasse
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.chat_tools.open_chat_manager import open_chat_manager


class TestOpenChatRequestJoinHandler(CommonTest, BaseOpenChatTestClasse):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.request_join

    def test_request_join_with_no_admin_connected(self, client: TestClient):
        chat_id, _ = self.create_new_open_chat(client)
        user_id = "guess_user_id"
        req_data = self.get_request_join_data(chat_id, user_id)

        with client.websocket_connect(f"{self.route}{chat_id}/{user_id}") as wb:
            wb.send_json(req_data.model_dump())
            resp_data = wb.receive_json()

            assert resp_data.get('type') == open_chat_msg_type.admin_not_conneceted
            assert "admin not connected" in resp_data.get('msg')


    def test_user_request_join(self, client: TestClient):
        chat_id, owner_id = self.create_new_open_chat(client)
        user_id = "guess_user_id"
        req_data = self.get_request_join_data(chat_id, user_id)

        add_to_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=open_chat_msg_type.open_chat_add,
            user_id=owner_id,
            user_name="owner"
        )

        with client.websocket_connect(f"{self.route}{chat_id}/{owner_id}") as admin_wb:
            admin_wb.send_json(add_to_data.model_dump())
            admin_wb.receive_json()

            with client.websocket_connect(f"{self.route}{chat_id}/{user_id}") as guess_wb:
                guess_wb.send_json(req_data.model_dump())
                res_to_join_data = admin_wb.receive_json()
                request_sent_data = guess_wb.receive_json()

                assert res_to_join_data.get('type') == open_chat_msg_type.request_join
                assert res_to_join_data.get('chat_id')
                assert res_to_join_data.get('user_id')
                assert res_to_join_data.get('user_name')

                assert request_sent_data.get('type') == open_chat_msg_type.request_join_sent
                assert request_sent_data.get('chat_id')
                assert f"to join sent for {chat_id}" in request_sent_data.get('msg')

                # user send request join again     
                with client.websocket_connect(f"{self.route}{chat_id}/{user_id}") as guess_wb1:
                    guess_wb1.send_json(req_data.model_dump())
                    res_to_join_data = admin_wb.receive_json()
                    request_sent_data = guess_wb1.receive_json()

                    assert res_to_join_data.get('type') == open_chat_msg_type.request_join
                    assert res_to_join_data.get('chat_id')
                    assert res_to_join_data.get('user_id')
                    assert res_to_join_data.get('user_name')

                    assert request_sent_data.get('type') == open_chat_msg_type.request_join_sent
                    assert request_sent_data.get('chat_id')
                    assert f"to join sent for {chat_id} again" in request_sent_data.get('msg')

                    assert len(open_chat_manager.chat_user_sockets.get(chat_id)) == 1
                    assert len(open_chat_manager.user_request_sockets.get(chat_id)) == 1
                    assert len(
                        open_chat_manager.user_request_sockets
                        .get(chat_id)
                        .get(user_id)
                    ) == 2