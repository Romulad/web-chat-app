import { useEffect, useRef, useState } from "react"
import { openChatReqDataScheme, openChatRespDataScheme, openChatUser } from "../../../lib/definitions"
import { openChatConnectionMsgType } from "../../../lib/constant"
import { getOpenChatSocketRoute } from "../../../lib/socketRoutes"
import { parseSocketData } from "../../../lib/functions"
import classes from "../../../lib/classes"


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

    useEffect(()=>{
        const websocket = new WebSocket(getOpenChatSocketRoute());

        websocket.addEventListener('open', (_)=>{
            ws.current = websocket;
            sendAskToJoinReq();
        })

        websocket.addEventListener('message', (ev)=>{
            const respData = parseSocketData(ev.data);
            setIsInAction(false);
            setSocketResp(respData);
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
                
                <></>
            }
        </div>
    )
}