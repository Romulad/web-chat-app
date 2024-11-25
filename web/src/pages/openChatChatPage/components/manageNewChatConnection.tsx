import { useState } from "react"

import { openChatReqDataScheme, openChatRespDataScheme, openChatUser } from "../../../lib/definitions"
import { openChatConnectionMsgType } from "../../../lib/constant"
import { getOpenChatSocketRoute } from "../../../lib/socketRoutes"
import { updateUserNotAllowedChatIds, updateUseropenChatData } from "../../../lib/functions"
import classes from "../../../lib/classes"
import OpenChatInterface from "./openChatInterface"
import { useWebSocket } from "../../../hooks"


type ManageNewChatConectionProps = {
    userData: openChatUser,
    chatId: string,
}

export default function ManageNewChatConection(
    {userData, chatId} : ManageNewChatConectionProps
){
    const socketUrl = getOpenChatSocketRoute(chatId, userData.userId);
    const { ws, isInAction } = useWebSocket(socketUrl, onOnpen, onMessage);
    const [displayingMsg, setDisplayingMsg] = useState('Attempting connection...');
    const [socketResp, setSocketResp] = useState<openChatRespDataScheme>();
    const [fullChatData, setFullChatData] = useState<openChatRespDataScheme>();

    function sendAskToJoinReq(ws?: WebSocket){
        const data : openChatReqDataScheme = {
            chat_id: chatId, 
            data: "", 
            type: openChatConnectionMsgType.request_join,
            user_id: userData.userId,
            user_name: userData.name,
            is_owner: false
        }
        ws?.send(JSON.stringify(data));
        setDisplayingMsg('Asking to join...');
    }

    function onOnpen(_: Event, ws?: WebSocket){
        sendAskToJoinReq(ws)
    }

    function onMessage(respData: openChatRespDataScheme){
        setSocketResp(respData);

        if (
            respData?.type === openChatConnectionMsgType.added_to_open_chat
        ){
            if(respData.chat_users){
                setFullChatData(respData);
                updateUseropenChatData(
                    chatId, respData.chat_name || "", respData.created_at || "", false 
                )
            }
        }else if (
            respData?.type === openChatConnectionMsgType.request_not_approved
        ){
            updateUserNotAllowedChatIds(chatId)
        }
    }

    return(
        fullChatData ?
        <OpenChatInterface 
        chatId={chatId}
        fullChatData={fullChatData}
        ws={ws}/> :

        <div className="h-screen flex items-center justify-center text-center">
            {
                isInAction ? (
                    <p className={"animate-pulse"}>
                        {displayingMsg}
                    </p>
                ) : 
                
                socketResp?.type === openChatConnectionMsgType.error ? (
                    <p>{socketResp.msg}</p>
                ) : 
                
                socketResp?.type === openChatConnectionMsgType.admin_not_conneceted ? (
                    <div className="flex flex-col gap-5">
                        <div>
                            <b>{socketResp.msg}</b>
                            <p>Ask an admin to connect on the chat and ask to join again</p>
                        </div>
                        
                        <button className={classes.btn.blue}
                        onClick={()=>{sendAskToJoinReq(ws)}}>
                            Ask to join
                        </button>
                    </div>
                ) : 
                
                socketResp?.type === openChatConnectionMsgType.request_join_sent ? (
                    <div>
                        <b>{socketResp.msg}</b>
                        <p>Waiting for an admin to accept your request...</p>
                    </div>
                ) :

                socketResp?.type === openChatConnectionMsgType.request_approved ? (
                    <div>
                        <p className="text-green-500">
                            Your request to join {socketResp.chat_id} 
                            have been approved by an admin
                        </p>
                    </div>
                ) :

                socketResp?.type === openChatConnectionMsgType.request_not_approved ? (
                    <div>
                        <p className="text-red-500">
                            Your request to join {socketResp.chat_id} 
                            have been rejected by an admin
                        </p>
                    </div>
                ) :

                <></>
            }
        </div>
    )
}