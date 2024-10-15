from fastapi.testclient import TestClient
from fastapi import status

from ..app.chat_tools.open_chat_manager import open_chat_manager
from ..app.req_resp_models import OpenChatInitSchema


class TestCreateNewOpenChatRoute:
    route = "/open-chat/init"

    def test_create_new_open_chat(self, client: TestClient):
        data = [
            {
                "chat_id": "randomId",
                "initiator_id": "superuserid",
                "initiator_name": "My name",
            },
            {
                "chat_id": "randomId2",
                "initiator_id": "superuserid",
                "initiator_name": "My name",
            }
        ]
        for chat_data in data:
            resp = client.post(self.route, json=chat_data)
            assert resp.status_code == status.HTTP_200_OK
        
        assert open_chat_manager.chats.get("randomId")
        assert len(open_chat_manager.chats) == 2
        assert open_chat_manager.chats['randomId'][0]['is_owner'] == True
    

class TestDeleteOpenChatRoute:
    route = "/open-chat/"

    def test_delete_open_chat_with_invalid_id(self, client:TestClient):
        resp = client.delete(self.route + "fakeId")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_open_chat(self, client:TestClient):
        open_chat_manager.create_new_chat(
            OpenChatInitSchema(
                chat_id="randomId",
                initiation_date="",
                initiator_id="myUserId",
                initiator_name="my name",
            )
        )

        resp = client.delete(self.route + "randomId")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert len(open_chat_manager.chats) == 0