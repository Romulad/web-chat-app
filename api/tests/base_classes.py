import datetime

from ..app.chat_tools.open_chat_manager import open_chat_manager
from ..app.req_resp_models import OpenChatInitSchema
from ..app.schemas import OpenChatUser

class BaseOpenChatClasse:

    def create_new_open_chat(self):
        new_chat_data = OpenChatInitSchema(
            chat_id="chat-testid",
            initiation_date=datetime.datetime.now().isoformat(),
            initiator_id="owern-ownerid",
            initiator_name="owner",
        )
        open_chat_manager.create_new_chat(new_chat_data)

        return "chat-testid", "owern-ownerid"

    def add_user_to_open_chat(self, chat_id, user_id, user_name="", is_owner=False):
        assert (chat_users := open_chat_manager.chats.get(chat_id))
        chat_users.append(OpenChatUser(
            user_id=user_id,
            is_owner=is_owner,
            name=user_name,
            created_at=datetime.datetime.now().isoformat()
        ))
        open_chat_manager.chats[chat_id] = chat_users
    
    def get_open_chat_user_data_or_none(self, chat_id, user_id):
        chat_users = open_chat_manager.chats.get(chat_id)

        if not chat_users:
            return None

        for chat_user in chat_users:
            if chat_user.user_id == user_id:
                return chat_user
        
        return None