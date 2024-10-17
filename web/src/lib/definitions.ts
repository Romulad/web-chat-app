
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
}

export type openChatOneData = {
    isOwner: boolean,
    chatId: string
}

export type openChatData = openChatOneData[]

export type openChatRespDataScheme = {
    msg?: string;
    chat_id: string;
    type: string
}