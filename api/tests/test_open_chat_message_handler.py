from fastapi.testclient import TestClient

from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type
from ..app.req_resp_models import OpenChatMsgDataSchema
from ..app.utils.functions import get_chat_users_from_redis_or_none


class TestOpenChatMessageHandler(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.new_message