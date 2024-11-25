
export type createOpenChatResp = {
    chat_id: string;
    initiator_id: string;
    initiator_name: string;
    initiation_date: string;
}

export type openChatUser = {
    userId: string;
    name: string;
}

export type openChatReqDataScheme = {
    type: string;
    data: Record<string, any> | string | number | Array<any>;
    user_id: string;
    chat_id: string;
    user_name: string;
    is_owner?: boolean;
    owner_id?: string;
}

export type openChatOneData = {
    isOwner: boolean,
    chatId: string,
    chatName: string,
    date: string
}

export type openChatData = openChatOneData[]

export type openChatRespDataScheme = {
    msg?: string;
    chat_id: string;
    type: string;
    data?: Array<any> | string | object;
    user_name?: string;
    user_id?: string;
    chat_users?: Array<connectedOpenChatUserRespData>;
    owner_name?: string,
    chat_msgs?: OpenChatMsg[],
    created_at?: string,
    chat_name?: string,
    connected_users?: string[]
}

export type connectedOpenChatUserRespData = {
    user_id: string;
    is_owner: boolean;
    name: string;
    created_at: string;
}

export type OpenChatMsg = {
    text: string,
    name: string,
    userId: string
}

export type UserTokenResp = {
    access_token: string,
    token_type: string
}

export type UserDataResp = {
    id: string,
    email: string,
    first_name: string,
    last_name: string,
    created_at: string,
}

export type UserChatHistoryResp = {
    chat_id: string;
    unread_count: number;
    unread_user_id: string;
    last_message: string;
    friend: UserDataResp;
    last_updated: string;
}[]

export type UserListResp = UserDataResp[]