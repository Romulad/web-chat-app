import datetime

import redis
from fastapi.testclient import TestClient

from ..app.chat_tools.open_chat_manager import open_chat_manager
from ..app.req_resp_models import OpenChatInitSchema, OpenChatMsgDataSchema
from ..app.schemas import OpenChatUser
from ..app.redis import redis_key
from ..app.utils.constants import open_chat_msg_type
from ..app.utils.functions import (
    parse_json, 
    stringify, 
    get_chat_users_from_redis_or_none
)

class BaseOpenChatTestClasse:

    def create_new_open_chat(self, client: TestClient):
        route = "/open-chat/init"
        
        new_chat_data = OpenChatInitSchema(
            chat_id="chat-testid",
            initiation_date=datetime.datetime.now().isoformat(),
            initiator_id="owern-ownerid",
            initiator_name="owner",
            chat_name="Group"
        ).model_dump()
        client.post(route, json=new_chat_data)

        return "chat-testid", "owern-ownerid"
        

    def get_request_join_data(self, chat_id, user_id):        
        request_data = OpenChatMsgDataSchema(
            chat_id=chat_id,
            data="",
            is_owner=False,
            type=open_chat_msg_type.request_join,
            user_id=user_id,
            user_name="Test name",
        )
        return request_data


    def add_user_to_open_chat(
        self, 
        chat_id, 
        user_id, 
        redis_c: redis.Redis,
        user_name="", 
        is_owner=False,
    ):
        assert (chat_users := redis_c.hget(redis_key.chats, chat_id))

        parsed_data = parse_json(chat_users)
        parsed_data.append(OpenChatUser(
            user_id=user_id,
            is_owner=is_owner,
            name=user_name,
            created_at=datetime.datetime.now().isoformat()
        ).model_dump())

        redis_c.hset(redis_key.chats, chat_id, stringify(parsed_data))
    

    def get_open_chat_user_data_or_none(
            self, 
            chat_id, 
            user_id, 
            redis_c: redis.Redis
    ):
        chat_users = get_chat_users_from_redis_or_none(redis_c, chat_id)

        if not chat_users:
            return None

        for chat_user in chat_users:
            validate_data = OpenChatUser(**chat_user)
            if validate_data.user_id == user_id:
                return validate_data
        
        return None