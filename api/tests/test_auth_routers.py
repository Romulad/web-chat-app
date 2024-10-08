from fastapi import status
from fastapi.testclient import TestClient
from pymongo.database import Database

from .utils import find_msg_in_resp
from ..app.database import db_collection_names
from ..app.schemas import UserWithPassword

class TestCreatAccountRoute:
    route = "/auth/sign-up"

    def test_email_validation(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"first_name": "Foo Bar", "password": "The Foo Barters"},
        )

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Field required" in find_msg_in_resp(resp.json())


    def test_email_format_validation(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"email": "testmail.com", "first_name": "Foo Bar", "password": "The Foo Barters"},
        )

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "email" in find_msg_in_resp(resp.json())    


    def test_duplicate_user_validation(
        self, client: TestClient, db: Database
    ):
        collection = db.get_collection(db_collection_names.users)
        collection.insert_one({"email": "test@mail.com"})

        resp = client.post(
            self.route,
            json={"email": "test@mail.com", "first_name": "Foo Bar", "password": "The Foo Barters"},
        )

        assert resp.status_code == status.HTTP_409_CONFLICT


    def test_first_name_validation(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"email": "test@gmail.com", "first_name": "F", "password": "The Foo Barters"},
        )

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "at least 3 characters" in find_msg_in_resp(resp.json())


    def test_password_validation(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"email": "test@gmail.com", "first_name": "Foo"},
        )

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Field required" in find_msg_in_resp(resp.json())


    def test_password_lenght_validation(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"email": "test@gmail.com", "first_name": "Foo", "password": "test"},
        )

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "at least 8 characters" in find_msg_in_resp(resp.json())


    def test_user_creation(self, client: TestClient):
        resp = client.post(
            self.route,  
            json={"email": "test@gmail.com", "first_name": "Foo", "password": "testpassword"},
        )

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.json().get('access_token')


class TestLoginRoute:
    route = "/auth/sign-in"

    def test_invalid_user(self, client: TestClient, db: Database):
        resp = client.post(
            self.route,
            data={"username": "test@gmail.com", "password": "testpassword"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_invalid_password(self, client: TestClient, db: Database):
        user = UserWithPassword(
            email="test@gmail.com",
            first_name="test",
            password="testpassword"
        )
        collection = db.get_collection(db_collection_names.users)
        collection.insert_one(user.model_dump())

        resp = client.post(
            self.route,
            data={"username": "test@gmail.com", "password": "fakepassw"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_access_token(self, client: TestClient, db: Database):
        user = UserWithPassword(
            email="test@gmail.com",
            first_name="test",
            password="testpassword"
        )
        collection = db.get_collection(db_collection_names.users)
        collection.insert_one(user.model_dump())

        resp = client.post(
            self.route,
            data={"username": "test@gmail.com", "password": "testpassword"},
        )

        assert resp.status_code == status.HTTP_200_OK
        assert resp.json().get('access_token')