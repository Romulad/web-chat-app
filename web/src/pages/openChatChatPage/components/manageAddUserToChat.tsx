import { useState } from "react";

import { useWebSocket } from "../../../hooks";
import { openChatConnectionMsgType } from "../../../lib/constant";
import { 
    openChatReqDataScheme, 
    openChatRespDataScheme, 
} from "../../../lib/definitions";
import { getOpenChatSocketRoute } from "../../../lib/socketRoutes";
import OpenChatInterface from "./openChatInterface";
import { getChatData, getUserOpenChatInfo } from "../../../lib/functions";
import { useChatDataContextValue } from "../../../context/chatDataContext";


export default function ManageAddUserToChat(){
    const { chatId, fullChatData, setFullChatData } = useChatDataContextValue();

    const chatData = getChatData(chatId);
    const userData = getUserOpenChatInfo();

    const socketUrl =  getOpenChatSocketRoute(chatId, userData?.userId || "");
    const {ws, isInAction, setIsInAction, initializing} = useWebSocket(
        socketUrl, onOpen, onMessage
    );
    const [webSocketResp, setWebSocketResp] = useState<openChatRespDataScheme>();
    const [displayingMsg, setDisplayingMsg] = useState("");

    function onOpen(_: Event, ws?: WebSocket){
        if(!chatData || !userData ){
            return
        }

        const data : openChatReqDataScheme = {
            chat_id: chatData.chatId,
            data: "",
            type: openChatConnectionMsgType.open_chat_add,
            user_id: userData.userId,
            user_name: userData.name,
            is_owner: chatData.isOwner,
        }
        if(ws)
            ws.send(JSON.stringify(data));
            setIsInAction(true);
            setDisplayingMsg(`Connecting to chat ${chatData.chatName}...`);
    }

    function onMessage(data: openChatRespDataScheme){
        if (
            data?.type === openChatConnectionMsgType.added_to_open_chat
        ){
            if(data.chat_users){
                setFullChatData(data);
            }
        }else{
            setWebSocketResp(data);
        }
    }

    return(
        !initializing && fullChatData ?
        <OpenChatInterface ws={ws} /> :
        
        <div className="h-screen flex items-center justify-center text-center">
            {
                initializing ? (
                    <p className={"animate-pulse"}>
                        Attempting connection
                    </p>
                ) :
                
                isInAction ? (
                    <p className={"animate-pulse"}>
                        {displayingMsg}
                    </p>
                ) :

                webSocketResp?.type === openChatConnectionMsgType.error ||
                webSocketResp?.type === openChatConnectionMsgType.not_allowed_user ? (
                    <p>{webSocketResp.msg}</p>
                ) :

                <></>
            }
        </div>
    )
}