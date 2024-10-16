from collections import namedtuple

SocketMsgType = namedtuple("SocketMsgType", ['msg', 'init', 'open_chat_add'])
socket_msg_type = SocketMsgType(
    msg='msg',
    init='init',
    open_chat_add="open_chat_add"
)

OpenChatMsgType = namedtuple(
    "OpenChatMsgType", 
    ['open_chat_add', 'error', "added_to_open_chat", 
    "notify_new_user", "request_join", "request_join_sent", 
    "notification", "admin_not_conneceted", "request_approved", "request_not_approved"]
)
open_chat_msg_type = OpenChatMsgType(
    open_chat_add="open_chat_add",
    error="error",
    added_to_open_chat="added_to_open_chat",
    notify_new_user="notify_new_user",
    request_join="request_join",
    request_join_sent="request_join_sent",
    admin_not_conneceted="admin_not_conneceted",
    request_approved="request_approved",
    request_not_approved="request_not_approved",
    notification='notification'
)