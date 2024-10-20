
export const getCreateAccountRoute = () =>{
    return "auth/sign-up";
}

export const getCreateOpenChatRoute = () =>{
    return "open-chat/init";
}

export const getDeleteOpenChatRoute = (chatId: string) => {
    return `open-chat/${chatId}`
}