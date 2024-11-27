import React, { createContext, useContext, useState } from "react";
import { openChatRespDataScheme } from "../lib/definitions";

type chatDataContextType = {
    chatId: string,
    fullChatData: openChatRespDataScheme | null,
    setFullChatData: React.Dispatch<openChatRespDataScheme>
}

type chatDataContextProviderType = {
    children: React.ReactNode,
    chatId: string | null
}

const defaultValue : chatDataContextType = {
    chatId: "",
    fullChatData: null,
    setFullChatData: () => {}
}

const chatDataContext = createContext<chatDataContextType>(defaultValue);

export function useChatDataContextValue(){
    const chatData = useContext(chatDataContext);
    return chatData
}

export function ChatDataContextProvider(
    { children, chatId } : chatDataContextProviderType
){
    if(!chatId){
        return <></>
    }

    const [fullChatData, setFullChatData] = useState<openChatRespDataScheme>();
    
    const providerValue : chatDataContextType = {
        chatId,
        fullChatData: fullChatData || null,
        setFullChatData
    }

    return(
        <chatDataContext.Provider value={providerValue}>
            {children}
        </chatDataContext.Provider>
    )
}