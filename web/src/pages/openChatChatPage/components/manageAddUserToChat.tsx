import { useState } from "react";

import { useWebSocket } from "../../../hooks";
import { openChatConnectionMsgType } from "../../../lib/constant";
import { 
    openChatOneData, 
    openChatReqDataScheme, 
    openChatRespDataScheme, 
    openChatUser 
} from "../../../lib/definitions";
import { getOpenChatSocketRoute } from "../../../lib/socketRoutes";
import OpenChatInterface from "./openChatInterface";


export default function ManageAddUserToChat(
    {
        chatData, 
        userData
    } : {chatData: openChatOneData, userData: openChatUser}
){
    const socketUrl =  getOpenChatSocketRoute(chatData.chatId, userData.userId);
    const {ws, isInAction, setIsInAction, initializing} = useWebSocket(
        socketUrl, onOpen, onMessage
    );
    const [webSocketResp, setWebSocketResp] = useState<openChatRespDataScheme>();
    const [displayingMsg, setDisplayingMsg] = useState("");
    const [fullChatData, setFullChatData] = useState<openChatRespDataScheme>();

    function onOpen(_: Event, ws?: WebSocket){
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
            setDisplayingMsg('Connecting to chat...');
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
        <OpenChatInterface 
        fullChatData={fullChatData}
        chatId={chatData.chatId}
        ws={ws} /> :
        
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