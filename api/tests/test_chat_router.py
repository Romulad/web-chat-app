import datetime

from fastapi.testclient import TestClient
from pymongo.database import Database
from fastapi import status, WebSocketDisconnect
import pytest

from .common_peformed import AuthenticationTests
from .base import BaseTestClass
from ..app.schemas import UserWithPassword, ChatMetaData, ChatMessage
from ..app.database import db_collection_names
from ..app.utils.security import create_user_token
from .utils import get_auth_header
from ..app.response_model import SocketDataSchema


class TestChatHistoryRoute(AuthenticationTests):
    route = "/chat/histories"

    def test_get_histories_new_user(self, client: TestClient, db: Database):
        user = UserWithPassword(
            email="test@gmail.com", 
            first_name="Moi", 
            password="testpassword"
        )
        collection = db.get_collection(db_collection_names.users)
        created = collection.insert_one(user.model_dump())
        token = create_user_token(str(created.inserted_id))

        resp = client.get(self.route, headers=get_auth_header(token))
        assert resp.status_code == status.HTTP_200_OK


    def test_get_chat_histories(self, client: TestClient, db:Database):
        first_user = UserWithPassword(
            email="test@gmail.com", 
            first_name="Moi", 
            password="testpassword"
        )
        second_user = UserWithPassword(
            email="test@gmail22.com", 
            first_name="Toi", 
            password="testpassword"
        )

        collection = db.get_collection(db_collection_names.users)
        created = collection.insert_many([first_user.model_dump(), second_user.model_dump()])
        [id1, id2] = created.inserted_ids

        metadata_collection = db.get_collection(db_collection_names.chat_metadata)
        metadata = ChatMetaData(
            chat_id="testid",
            first_user_id=str(id1),
            last_message="our last message",
            last_updated=datetime.datetime.now(datetime.timezone.utc),
            second_user_id=str(id2),
        )
        metadata_collection.insert_one(metadata.model_dump())

        resp = client.get(self.route, headers=get_auth_header(create_user_token(str(id1))))
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json().get('data'))


class TestChatMessageRoute(AuthenticationTests, BaseTestClass):
    route = "/chat/ws"
    use_socket = True

    def test_connection_initialization(
        self, client:TestClient, db: Database
    ):
        sockets = []
        for user_id in self.create_users(db):
            route = self.route + f"?token={create_user_token(user_id)}"
            with client.websocket_connect(route) as websocket:
                websocket.send_json({"data": "", "type": "init"})
                data = websocket.receive_text()
                assert data.lower() == "connected"
                sockets.append(websocket)
                
        for socket in sockets:
            socket.close()


    def test_send_message_with_existing_metadata(
        self, client:TestClient, db: Database
    ):
        user1_id = self.create_user(db)
        user2_id = self.create_user(db, "test45@gmail22.com")

        metadata = ChatMetaData(
            chat_id="justtestId",
            first_user_id=user1_id,
            last_message="your message",
            last_updated=datetime.datetime.now(),
            second_user_id=user2_id,
        )
        db.get_collection(
            db_collection_names.chat_metadata
        ).insert_one(
            metadata.model_dump()
        )

        route = self.route + f"?token={create_user_token(user1_id)}"
        with client.websocket_connect(route) as websocket:
                msg_data = SocketDataSchema(
                    chat_id="justtestId",
                    data="Hello user 2",
                    to_user_id=user2_id,
                    type="msg"
                )
                websocket.send_json(msg_data.model_dump())
                data = websocket.receive_json()
                assert data.get('chat_id') == "justtestId"
                assert data.get('msg')
                assert data.get('sender_id')
                websocket.close()
        
        assert db.get_collection(
            db_collection_names.chat_messages
        ).find({"chat_id": "justtestId"}).to_list()

        assert (mta_data := db.get_collection(
            db_collection_names.chat_metadata
        ).find_one({"chat_id": "justtestId"}))

        assert mta_data.get('last_message') == "Hello user 2"
    

    def test_send_message(
        self, client:TestClient, db: Database
    ):
        user1_id = self.create_user(db)
        user2_id = self.create_user(db, "test45@gmail22.com")

        route = self.route + f"?token={create_user_token(user1_id)}"
        with client.websocket_connect(route) as websocket:
                msg_data = SocketDataSchema(
                    chat_id="justtestId",
                    data="Hello user 2",
                    to_user_id=user2_id,
                    type="msg"
                )
                websocket.send_json(msg_data.model_dump())
                data = websocket.receive_json()
                assert data.get('chat_id') == "justtestId"
                assert data.get('msg')
                assert data.get('sender_id')
                websocket.close()
        
        assert db.get_collection(
            db_collection_names.chat_messages
        ).find({"chat_id": "justtestId"}).to_list()
        assert db.get_collection(
            db_collection_names.chat_metadata
        ).find_one({"chat_id": "justtestId"})


    def test_send_message_with_invalid_data(
        self, client:TestClient, db: Database
    ):
        user1_id = self.create_user(db)

        route = self.route + f"?token={create_user_token(user1_id)}"
        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect(route) as websocket:
                    msg_data = {"chat_id": "testid", "type":"msg", "data": ""}
                    websocket.send_json(msg_data)
                    data = websocket.receive_json()
                    assert data.get('chat_id') == "justtestId"
                    assert data.get('msg')
                    assert data.get('sender_id')
                    websocket.close()


class TestGetMessages(AuthenticationTests, BaseTestClass):
    route = "/chat/messages/testchatid"
    chat_id = "testchatid"

    def test_get_messages(self, client: TestClient, db:Database):
        collection = db.get_collection(db_collection_names.chat_messages)
        mta_collection = db.get_collection(db_collection_names.chat_metadata)

        user1_id = self.create_user(db)
        user2_id = self.create_user(db, "test123457@gmail.com")

        self.generate_chat_messages(db, self.chat_id, user1_id, user2_id)
        mta_data = ChatMetaData(
            chat_id=self.chat_id,
            first_user_id=user1_id,
            last_message="test",
            last_updated=datetime.datetime.now(),
            second_user_id=user2_id,
            unread_count=5,
            unread_user_id=user1_id
        )
        mta_collection.insert_one(mta_data.model_dump())

        token = create_user_token(user1_id)
        resp = client.get(self.route, headers=get_auth_header(token))

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json().get('data')) == 6

        data = collection.find({
            "$and": [
                {"chat_id": self.chat_id},
                {"read": True}
            ]
        }).to_list()
        mta_db_data = mta_collection.find_one({"chat_id": self.chat_id})

        assert len(data) == 3
        assert mta_db_data
        assert mta_db_data.get('unread_count') == 0
        assert mta_db_data.get('unread_user_id') == ""