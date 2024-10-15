import datetime

from fastapi import HTTPException, status

from ..req_resp_models import OpenChatInitSchema


class OpenChatManager:
    chats : dict[str, list] = {}

    def create_new_chat(self, chat_data:OpenChatInitSchema):
        self.chats[chat_data.chat_id] = [
            {
                "user_id": chat_data.initiator_id, 
                "is_owner": True, 
                "name": chat_data.initiator_name,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]
    
    def delete_chat(self, chat_id:str):
        if self.chats.get(chat_id):
            del self.chats[chat_id]
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Chat can't be found"
            )


open_chat_manager = OpenChatManager()