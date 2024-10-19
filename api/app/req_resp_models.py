import datetime
from pydantic import BaseModel

from .schemas import UserWithId, ChatMessage

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatHistory(BaseModel):
    chat_id: str
    unread_count: int = 0
    unread_user_id: str = ""
    last_message: str
    friend: UserWithId
    last_updated: datetime.datetime


class ChatHistories(BaseModel):
    data: list[ChatHistory] = []


class ChatMessages(BaseModel):
    data: list[ChatMessage]


class SocketDataSchema(BaseModel):
    type: str = "msg"
    data: str | bytes
    chat_id: str = ""
    to_user_id: str = ""


class ChatResponse(BaseModel):
    chat_id: str
    msg: str
    sender_id: str
    

class OpenChatInitSchema(BaseModel):
    chat_id: str
    initiator_id: str
    initiator_name: str
    initiation_date: str = ""


class OpenChatMsgDataSchema(BaseModel):
    type: str
    data: dict | str | int | list
    user_id: str
    chat_id: str
    user_name: str
    is_owner: bool = False