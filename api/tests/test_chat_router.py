import datetime

from fastapi.testclient import TestClient
from pymongo.database import Database
from fastapi import status

from .common_peformed import AuthenticationTests
from ..app.schemas import UserWithPassword, ChatMetaData
from ..app.database import db_collection_names
from ..app.utils.security import create_user_token
from .utils import get_auth_header


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
        assert len(resp.json().get('datas'))


        


