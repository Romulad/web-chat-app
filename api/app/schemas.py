from datetime import datetime, timezone
from typing_extensions import Annotated

from fastapi import WebSocket
from pydantic import (
    BaseModel, EmailStr, Field, field_serializer, ConfigDict
)
from pydantic.functional_validators import BeforeValidator

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


class UserWithId(User):
    id: Annotated[str, BeforeValidator(str)] = Field(default="", validation_alias="_id", )


class UserFriend(BaseModel):
    first_user_id: str
    second_user_id: str
    chat_id: str
    relation_start_at: datetime = None
    inviter_user_id: str

    @field_serializer('relation_start_at')
    def serialize_relation_start_at(self, relation_start_at: datetime | None):
        return relation_start_at.isoformat() if relation_start_at else relation_start_at


class ChatMessage(BaseModel):
    chat_id: str
    sender_id: str
    receiver_id: str
    read: bool = False
    text: str = ""
    read_at: datetime | None = None
    created_at: datetime = datetime.now(timezone.utc)

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime):
        return created_at.isoformat()

    @field_serializer('read_at')
    def serialize_read_at(self, read_at: datetime | None):
        return read_at.isoformat() if read_at else read_at


class ChatMetaData(BaseModel):
    id: Annotated[str, BeforeValidator(str)] = Field(default="", validation_alias="_id", )
    chat_id: str
    unread_count: int = 0
    unread_user_id: str = ""
    first_user_id: str
    second_user_id: str
    last_message: str
    last_updated: datetime

    @field_serializer('last_updated')
    def serialize_last_updated(self, last_updated: datetime):
        return last_updated.isoformat()
    
class OpenChatUser(BaseModel):
    user_id: str
    is_owner: bool
    name: str
    websockets: list[WebSocket] = []
    created_at: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class OpenChatRequestJoin(BaseModel):
    chat_id: str
    user_id: str
    user_name: str
    websockets: list[WebSocket] = []

    model_config = ConfigDict(arbitrary_types_allowed=True)
