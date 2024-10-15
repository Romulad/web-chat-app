

export const homePath = "/";
export const createAccountPath = "/auth/create-account";
export const openChatPath = "/open-chat/:chatId"


export const getOpenChatPath = (chatId: string) => {
    return `/open-chat/${chatId}`
}