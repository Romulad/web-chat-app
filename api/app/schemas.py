from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field, field_serializer

from .utils.security import hash_passord


class User(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=3)
    last_name: str = ""
    created_at: datetime = datetime.now(timezone.utc)

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime):
        return created_at.isoformat()


class UserWithPassword(User):
    password: str = Field(min_length=8)

    @field_serializer('password')
    def serialize_password(self, password: str):
        return hash_passord(password)


class UserFriend(BaseModel):
    user_id: str
    friend_id: str
    chat_id: str
    relation_start_at: datetime = None


class ChatHistory(BaseModel):
    chat_id: str
    sender_id: str
    receiver_id: str
    created_at: datetime


class ChatMessage(ChatHistory):
    text: str = ""
    read: bool = False
    read_at: datetime = None