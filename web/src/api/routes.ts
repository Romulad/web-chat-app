
export const getCreateAccountRoute = () =>{
    return "auth/sign-up";
}

export const getCreateOpenChatRoute = () =>{
    return "open-chat/init";
}

export const getDeleteOpenChatRoute = (chatId: string, userId: string) => {
    return `open-chat/${chatId}/${userId}`
}

export const getAboutUserDataRoute = () => {
    return "auth/me"
}

export const getUserChatHistoriesRoute = () => {
    return "chat/histories"
}

export const getFindUserRoute = () => {
    return 'chat/find'
}