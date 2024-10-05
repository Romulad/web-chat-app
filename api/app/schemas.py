from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str = ""
    created_at: datetime = None


class UserWithPassword(User):
    password: str


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