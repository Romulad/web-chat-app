from pydantic import BaseModel

class OpenChatInitSchema(BaseModel):
    chat_id: str
    chat_name: str
    initiator_id: str
    initiator_name: str
    initiation_date: str = ""


class OpenChatMsgDataSchema(BaseModel):
    type: str
    data: dict | str | int | list
    user_id: str
    chat_id: str
    chat_name: str = ""
    user_name: str
    is_owner: bool = False
    owner_id: str = ""
    send_at: str = ""