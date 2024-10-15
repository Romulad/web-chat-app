from fastapi import APIRouter, WebSocket, status

from ..req_resp_models import OpenChatInitSchema
from ..chat_tools.open_chat_manager import open_chat_manager

router = APIRouter(prefix="/open-chat")


@router.post("/init", status_code=status.HTTP_201_CREATED)
async def create_new_open_chat(
    data: OpenChatInitSchema
):
    open_chat_manager.create_new_chat(data)
    return data


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_new_open_chat(
    chat_id
):
    open_chat_manager.delete_chat(chat_id)
    return ""