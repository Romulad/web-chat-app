from datetime import datetime

import pytest
from pydantic import ValidationError

from ..app import schemas


class TestUserSchema:
    def test_user_email_validation(self):
        data = {"email": "testgmail.com", "first_name": "myFirstname"}
        with pytest.raises(ValidationError):
            schemas.User(**data)

    def test_user_firstName_validation(self):
        data = {"email": "test@gmail.com", "last_name": "myLastName"}
        with pytest.raises(ValidationError):
            schemas.User(**data)
    
    def test_user_schema_field(self):
        data = {
            "email": "test@gmail.com", 
            "first_name": "myFirstname",
            "created_at": str(datetime.now())
        }

        result = schemas.User(**data)
        assert hasattr(result, "email")
        assert hasattr(result, "first_name")
        assert hasattr(result, "created_at")
        assert hasattr(result, "last_name")
        assert isinstance(result.created_at, datetime)


class TestUserWithPasswordSchema:
    def test_user_password_validation(self):
        data = {"email": "test@gmail.com", "first_name": "myLastName"}
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserWithPassword(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "password"


class TestUserFriendSchema:
    def test_user_id_validation(self):
        data = {"friend_id": "some_id", "chat_id": "some_id"}
        with pytest.raises(ValidationError):
            schemas.UserFriend(**data)
        
        # when `user_id` is not a valid str
        data = {"friend_id": "some_id", "chat_id": "some_id", "user_id": datetime.now()}
        with pytest.raises(ValidationError):
            schemas.UserFriend(**data)

    def test_friend_id_validation(self):
        data = {"user_id": "some_id", "chat_id": "some_id"}
        with pytest.raises(ValidationError):
            schemas.UserFriend(**data)
        
        # when `friend_id` is not a valid str
        data = {"user_id": "some_id", "chat_id": "some_id", "friend_id": datetime.now()}
        with pytest.raises(ValidationError):
            schemas.UserFriend(**data)
    
    def test_chat_id_validation(self):
        data = {"user_id": "some_id", "frien_id": "some_id"}
        with pytest.raises(ValidationError):
            schemas.UserFriend(**data)
        
        # when `chat_id` is not a valid str
        data = {"user_id": "some_id", "friend_id": "some_id", "chat_id": datetime.now()}
        with pytest.raises(ValidationError):
            schemas.UserFriend(**data)
    
    def test_user_friend_schema_field(self):
        data = {
            "user_id": "some_id", 
            "friend_id": "some_id",
            "chat_id": "some_id",
            "relation_start_at": str(datetime.now())
        }

        result = schemas.UserFriend(**data)
        assert hasattr(result, "user_id")
        assert hasattr(result, "friend_id")
        assert hasattr(result, "chat_id")
        assert hasattr(result, "relation_start_at")
        assert isinstance(result.relation_start_at, datetime)


class TestChatHistorySchema:
    def test_chat_id_validation(self):
        data = {"sender_id": "some_id", "receiver_id": "some_id", "created_at": str(datetime.now())}
        with pytest.raises(ValidationError) as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "chat_id"
        
        # when `chat_id` is not a valid str
        data = {
            "sender_id": "some_id", 
            "receiver_id": "some_id", 
            "created_at": str(datetime.now()),
            "chat_id": None
        }
        with pytest.raises(ValidationError, match="should be a valid string") as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "chat_id"

    def test_sender_id_validation(self):
        data = {"chat_id": "some_id", "receiver_id": "some_id", "created_at": str(datetime.now())}
        with pytest.raises(ValidationError) as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "sender_id"
        
        # when `chat_id` is not a valid str
        data = {
            "chat_id": "some_id", 
            "receiver_id": "some_id", 
            "created_at": str(datetime.now()),
            "sender_id": None
        }
        with pytest.raises(ValidationError, match="should be a valid string") as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "sender_id"
    
    def test_receiver_id_validation(self):
        data = {"chat_id": "some_id", "sender_id": "some_id", "created_at": str(datetime.now())}
        with pytest.raises(ValidationError) as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "receiver_id"
        
        # when `chat_id` is not a valid str
        data = {
            "chat_id": "some_id", 
            "sender_id": "some_id", 
            "created_at": str(datetime.now()),
            "receiver_id": None
        }
        with pytest.raises(ValidationError, match="should be a valid string") as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "receiver_id"
    
    def test_created_at_validation(self):
        data = {"chat_id": "some_id", "sender_id": "some_id", "receiver_id": "some_id"}
        with pytest.raises(ValidationError) as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "created_at"
        
        # when `chat_id` is not a valid str
        data = {
            "chat_id": "some_id", 
            "sender_id": "some_id", 
            "created_at": "some_str",
            "receiver_id": "some_id"
        }
        with pytest.raises(ValidationError, match="should be a valid datetime or date") as exc_info:
            schemas.ChatHistory(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "created_at"