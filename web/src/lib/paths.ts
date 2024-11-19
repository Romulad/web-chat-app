

export const homePath = "/";
export const openChatPath = "/open-chat/:chatId"
export const openChatHomePath = "/open-chat"

export const getOpenChatPath = (chatId: string) => {
    return `/open-chat/${chatId}`
}