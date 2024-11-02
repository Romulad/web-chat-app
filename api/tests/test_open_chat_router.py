import redis
from fastapi.testclient import TestClient
from fastapi import status

from ..app.chat_tools.open_chat_manager import open_chat_manager
from ..app.req_resp_models import OpenChatInitSchema, OpenChatMsgDataSchema
from ..app.utils.constants import open_chat_msg_type
from .open_chat_route_common_performed import CommonTest
from .base_classes import BaseOpenChatClasse
from ..app.redis import redis_key
from ..app.utils.functions import parse_json


class TestCreateNewOpenChatRoute:
    route = "/open-chat/init"

    def test_create_new_open_chat(
        self, 
        client: TestClient, 
        redis_c: redis.Redis
    ):
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
            assert resp.status_code == status.HTTP_201_CREATED
        
        chat_one = redis_c.hget(redis_key.chats, "randomId")
        chat_two = redis_c.hget(redis_key.chats, "randomId2")
        chat_one_owner = redis_c.hget(redis_key.chat_owners_ref, "randomId")
        chat_two_owner = redis_c.hget(redis_key.chat_owners_ref, "randomId")
        assert chat_one
        assert chat_two
        assert chat_one_owner
        assert chat_two_owner
        assert len(redis_c.hgetall(redis_key.chats)) == 2
        assert len(redis_c.hgetall(redis_key.chat_owners_ref)) == 2

        chat_one = parse_json(chat_one)
        chat_one_owner = parse_json(chat_one_owner)
        assert chat_one[0]['is_owner'] == True
        assert chat_one_owner["name"] == "My name"

        for chat_id in ["randomId", "randomId2"]:
            chat_msgs = parse_json(redis_c.hget(redis_key.chat_msgs, chat_id))
            assert isinstance(chat_msgs, list)


    def test_create_existing_open_chat(self, client: TestClient):
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
            assert resp.status_code == status.HTTP_201_CREATED

        existing_resp = client.post(self.route, json=data[0])
        assert existing_resp.status_code == status.HTTP_409_CONFLICT
        assert "id already exists" in existing_resp.json().get('detail')
    
    def test_create_chat_with_invalid_data(self, client: TestClient):
        data = [
            {
                "chat_id": "randomId",
                "initiator_id": "superuserid",
            },
            {
                "chat_id": "randomId2",
                "initiator_name": "My name",
            }
        ]
        for chat_data in data:
            resp = client.post(self.route, json=chat_data)
            assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteOpenChatRoute(BaseOpenChatClasse):
    route = "/open-chat/"

    
    def test_delete_open_chat_with_invalid_id(
        self, 
        client:TestClient, 
    ):
        resp = client.delete(self.route + "fakeId")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_open_chat(
        self, 
        client:TestClient,
        redis_c: redis.Redis
    ):
        chat_id, _ = self.create_new_open_chat(client)

        resp = client.delete(self.route + chat_id)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert redis_c.hget(redis_key.chats, chat_id) == None
        assert redis_c.hget(redis_key.chat_owners_ref, chat_id) == None
        assert redis_c.hget(redis_key.chat_msgs, chat_id) == None
        assert len(redis_c.hgetall(redis_key.chats)) == 0


class TestOpenChatAddToChat(CommonTest, BaseOpenChatClasse):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.open_chat_add

    def test_add_existing_user_to_open_chat(self, client:TestClient):
        chat_id, owner_id = self.create_new_open_chat()

        new_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id=owner_id,
            user_name="owner",
        )

        with client.websocket_connect(self.route + chat_id + "/" + owner_id) as wb:
            wb.send_json(new_msg_data.model_dump())
            added_data = wb.receive_json()
            assert added_data.get('type') == open_chat_msg_type.added_to_open_chat
            assert added_data.get('chat_id')
            assert len(added_data.get('chat_users')) == 1
            assert added_data.get('chat_users')[0]["user_id"] == owner_id
        
            with client.websocket_connect(self.route + chat_id + "/" + owner_id) as wb1:
                wb1.send_json(new_msg_data.model_dump())
                added_data1 = wb1.receive_json()
                assert added_data1.get('type') == open_chat_msg_type.added_to_open_chat
                assert added_data1.get('chat_id')
                assert len(added_data1.get('chat_users')) == 1
                assert added_data1.get('chat_users')[0]["user_id"] == owner_id
        
                assert len(open_chat_manager.chats.get(chat_id)) == 1
                assert len(open_chat_manager.chats.get(chat_id)[0].websockets) == 2


    def test_add_user_to_open_chat(self, client: TestClient):
        chat_id, _ = self.create_new_open_chat()
        self.add_user_to_open_chat(chat_id, "guess_user_id", "guess")
        new_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id="guess_user_id",
            user_name="guess",
        )

        with client.websocket_connect(self.route + chat_id + "/guess_user_id") as wb:
            wb.send_json(new_msg_data.model_dump())
            added_data = wb.receive_json()
            assert added_data.get('type') == open_chat_msg_type.added_to_open_chat
            assert added_data.get('chat_id')
            assert added_data.get('chat_users')
            assert added_data.get('connected_users')
            assert len(added_data.get('chat_users')) == 2
            assert len(added_data.get('connected_users')) == 1
            assert len(open_chat_manager.chats.get(chat_id)) == 2
    
    def test_add_not_allowed_user_to_open_chat(self, client: TestClient):
        chat_id, _ = self.create_new_open_chat()
        new_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id="guess_user_id",
            user_name="guess",
        )

        with client.websocket_connect(self.route + chat_id + "/guess_user_id") as wb:
            wb.send_json(new_msg_data.model_dump())
            added_data = wb.receive_json()
            assert added_data.get('type') == open_chat_msg_type.not_allowed_user
            assert "not allowed to acess this chat" in added_data.get('msg')
            assert len(open_chat_manager.chats.get(chat_id)) == 1
    

    def test_broadcast_on_new_add(self, client: TestClient):
        chat_id, owner_id = self.create_new_open_chat()
        self.add_user_to_open_chat(chat_id, "guess_id", "guess")
        self.add_user_to_open_chat(chat_id, "guess_id2", "guess")

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

        user2_msg_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            type=self.msg_type,
            user_id="guess_id2",
            user_name="guess2",
        )

        with client.websocket_connect(self.route + chat_id + "/" + owner_id) as wb:
            wb.send_json(owner_msg_data.model_dump())
            wb.receive_json()

            with client.websocket_connect(self.route + chat_id + "/guess_id") as wb1:
                wb1.send_json(user1_msg_data.model_dump())
                wb1.receive_json()

                added_one_data = wb.receive_json()
                assert added_one_data.get('type') == open_chat_msg_type.notify_new_user
                assert added_one_data.get('chat_id')
                assert added_one_data.get('user_name') == "guess"
                assert added_one_data.get('user_id')
                assert len(added_one_data.get('chat_users')) == 3
                assert len(added_one_data.get('connected_users')) == 2

                with client.websocket_connect(self.route + chat_id + "/guess_id2") as wb2:
                    wb2.send_json(user2_msg_data.model_dump())
                    wb2.receive_json()

                    added_two_data = [wb.receive_json(), wb1.receive_json()]
                    for data in added_two_data:
                        assert data.get('type') == open_chat_msg_type.notify_new_user
                        assert data.get('chat_id')
                        assert data.get('user_name') == "guess2"
                        assert data.get('user_id')
                        assert len(data.get('chat_users')) == 3
                        assert len(data.get('connected_users')) == 3