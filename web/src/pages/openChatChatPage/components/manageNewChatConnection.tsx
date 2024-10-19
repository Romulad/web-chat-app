import { useEffect, useRef, useState } from "react"

import { connectedOpenChatUserRespData, openChatReqDataScheme, openChatRespDataScheme, openChatUser } from "../../../lib/definitions"
import { openChatConnectionMsgType } from "../../../lib/constant"
import { getOpenChatSocketRoute } from "../../../lib/socketRoutes"
import { parseSocketData, updateUserNotAllowedChatIds, updateUseropenChatData } from "../../../lib/functions"
import classes from "../../../lib/classes"
import OpenChatInterface from "./openChatInterface"


type ManageNewChatConectionProps = {
    userData: openChatUser,
    chatId: string,
}

export default function ManageNewChatConection(
    {userData, chatId} : ManageNewChatConectionProps
){
    const [displayingMsg, setDisplayingMsg] = useState('Attempting connection...');
    const [isInAction, setIsInAction] = useState(true);
    const [socketResp, setSocketResp] = useState<openChatRespDataScheme>();
    const ws = useRef<WebSocket>();
    const [chatUsers, setChatUsers] = useState<Array<connectedOpenChatUserRespData>>();

    useEffect(()=>{
        const websocket = new WebSocket(getOpenChatSocketRoute());

        websocket.addEventListener('open', (_)=>{
            ws.current = websocket;
            sendAskToJoinReq();
        })

        websocket.addEventListener('message', (ev)=>{
            console.log("got message")
            const respData = parseSocketData(ev.data);
            setIsInAction(false);
            setSocketResp(respData);

            if (
                respData?.type === openChatConnectionMsgType.added_to_open_chat
            ){
                if(respData.chat_users){
                    setChatUsers(respData.chat_users);
                }
            }else if (
                respData?.type === openChatConnectionMsgType.request_approved
            ){
                updateUseropenChatData(chatId, false);
            }else if (
                respData?.type === openChatConnectionMsgType.request_not_approved
            ){
                updateUserNotAllowedChatIds(chatId)
            }
        })

        return () => { websocket.close() }
    }, [])

    function sendAskToJoinReq(){
        const data : openChatReqDataScheme = {
            chat_id: chatId, 
            data: "", 
            type: openChatConnectionMsgType.request_join,
            user_id: userData.userId,
            user_name: userData.name,
            is_owner: false
        }
        ws.current?.send(JSON.stringify(data));
        setDisplayingMsg('Asking to join...');
        setIsInAction(true);
    }

    return(
        chatUsers ?
        <OpenChatInterface 
        chatId={chatId}
        chatUsers={chatUsers}
        ws={ws.current}
        /> :

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
                        onClick={sendAskToJoinReq}>
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
                        <p>
                            Your request to join {socketResp.chat_id} 
                            have been approved by an admin
                        </p>
                    </div>
                ) :

                socketResp?.type === openChatConnectionMsgType.request_not_approved ? (
                    <div>
                        <p>
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