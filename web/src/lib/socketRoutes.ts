import { getBaseRoute } from "../api/constant"


export const getOpenChatSocketRoute = (chatId: string, userId: string) => {
    const baseRoute = getBaseRoute(true);
    return `${baseRoute}open-chat/ws/${chatId}/${userId}`
}