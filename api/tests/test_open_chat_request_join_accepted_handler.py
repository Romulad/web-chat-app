
from .base_classes import BaseOpenChatTestClasse
from .open_chat_route_common_performed import CommonTest
from ..app.utils.constants import open_chat_msg_type


class TestOpenChatRequestJoinApprovedHandler(BaseOpenChatTestClasse, CommonTest):
    route = "/open-chat/ws/"
    msg_type = open_chat_msg_type.request_approved