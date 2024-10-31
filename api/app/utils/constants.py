from collections import namedtuple

OpenChatMsgType = namedtuple(
    "OpenChatMsgType", 
    ['open_chat_add', 'error', "added_to_open_chat", 
    "notify_new_user", "request_join", "request_join_sent", 
    "notification", "admin_not_conneceted", "request_approved", "request_not_approved",
    "user_disconnect", "new_message", "chat_deleted", "not_allowed_user"]
)
open_chat_msg_type = OpenChatMsgType(
    open_chat_add="open_chat_add",
    error="error",
    added_to_open_chat="added_to_open_chat",
    not_allowed_user="not_allowed_user",
    notify_new_user="notify_new_user",
    request_join="request_join",
    request_join_sent="request_join_sent",
    admin_not_conneceted="admin_not_conneceted",
    request_approved="request_approved",
    request_not_approved="request_not_approved",
    notification='notification',
    user_disconnect="user_disconnect",
    new_message="new_message",
    chat_deleted="chat_deleted"
)