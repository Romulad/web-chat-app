import datetime
from pydantic import BaseModel

from .schemas import UserWithId

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
    datas: list[ChatHistory] = []