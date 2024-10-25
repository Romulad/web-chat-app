from fastapi import WebSocket
from pydantic import (
    BaseModel, ConfigDict
)
    
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
