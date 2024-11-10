from pydantic import BaseModel

    
class OpenChatUser(BaseModel):
    user_id: str
    is_owner: bool
    name: str
    created_at: str


class OpenChatRequestJoin(BaseModel):
    chat_id: str
    user_id: str
    user_name: str


class OpenChatMsg(BaseModel):
    send_at: str
    sender_id: str
    sender_name: str
    chat_id: str
    msg: str
