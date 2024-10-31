import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from pydantic import ValidationError

from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.utils.constants import open_chat_msg_type

class CommonTest:
    msg_type = open_chat_msg_type.open_chat_add
    
    def test_not_found_chat(self, client:TestClient):
        with client.websocket_connect(self.route + "not_found_id/" + "testid") as wb:
            msg_data = OpenChatMsgDataSchema(
                chat_id="not_found_id",
                type=self.msg_type,
                data="",
                is_owner=False,
                user_id="testid",
                user_name="Your name",
            )
            wb.send_json(msg_data.model_dump())
            recv_data = wb.receive_json()
            assert "not found" in recv_data.get("msg")
            assert recv_data.get('type') == open_chat_msg_type.error
    
    def test_with_invalid_data(self, client:TestClient):
        with pytest.raises(ValidationError) as exce:
            with client.websocket_connect(self.route + "not_found_id/" + "testid") as wb:
                msg_data = {
                    "chat_id": "not_found_id",
                    "is_owner": False,
                    "user_id": "testid",
                    "user_name": "Your name"
                }
                wb.send_json(msg_data)
        
        with pytest.raises(ValidationError) as exce1:
            with client.websocket_connect(self.route + "not_found_id/" + "testid") as wb1:
                msg_data = {
                    "data": "not_found_id",
                    "is_owner": False,
                    "user_id": "testid",
                    "user_name": "Your name"
                }
                wb1.send_json(msg_data)

    def test_with_invalid_params(self, client:TestClient):
        with pytest.raises(WebSocketDisconnect) as exce:
            with client.websocket_connect(self.route + "not_found_id") as wb:
                msg_data = {
                    "chat_id": "not_found_id",
                    "is_owner": False,
                    "user_id": "testid",
                    "user_name": "Your name"
                }
                wb.send_json(msg_data)
        
        with pytest.raises(WebSocketDisconnect) as exce1:
            with client.websocket_connect(self.route) as wb1:
                msg_data = {
                    "data": "not_found_id",
                    "is_owner": False,
                    "user_id": "testid",
                    "user_name": "Your name"
                }
                wb1.send_json(msg_data)
    