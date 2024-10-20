from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect

from ..req_resp_models import OpenChatInitSchema
from ..chat_tools.open_chat_manager import open_chat_manager

router = APIRouter(prefix="/open-chat")


@router.post(
    "/init", 
    status_code=status.HTTP_201_CREATED, 
    response_model=OpenChatInitSchema
)
async def create_new_open_chat(
    data: OpenChatInitSchema
):
    open_chat_manager.create_new_chat(data)
    return data


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_open_chat(
    chat_id
):
    await open_chat_manager.delete_chat(chat_id)
    return ""


@router.websocket("/ws")
async def open_chat_messages(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await open_chat_manager.on_new_message(websocket)
    except WebSocketDisconnect:
        await open_chat_manager.disconnect_user(websocket)
