from collections import namedtuple

SocketMsgType = namedtuple("SocketMsgType", ['msg', 'init'])
socket_msg_type = SocketMsgType(
    msg='msg',
    init='init',
)