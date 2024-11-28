import { OpenChatMsg } from "../../lib/definitions"
import { getUserOpenChatInfo } from "../../lib/functions"
import LocalMsgDisplay from "../localMsgDisplay"
import RemoteMsgDisplay from "../remoteMsgDisplay"


type completeMsgType = {
    chat_id: string;
    msg: string;
    send_at: string;
    sender_id: string
    sender_name: string
    extraMsg?: string[]
}

export default function OpenChatMessageDisplay(
    { openChatMsgs } : { openChatMsgs: OpenChatMsg[] }
){
    const userData = getUserOpenChatInfo();
    const msgsList : completeMsgType[] = [];
    let lastMsgUserId = "";
    
    openChatMsgs.map((data)=>{
        if(msgsList.length <= 0){
            msgsList.push(data)
            lastMsgUserId = data.sender_id;
            return
        }

        const lastMsg = msgsList[msgsList.length - 1];
        if(lastMsg.sender_id === data.sender_id){
            const updatedMsg = {
                ...lastMsg, 
                extraMsg: [...(lastMsg?.extraMsg || []), data.msg]
            }
            lastMsgUserId = data.sender_id;
            msgsList.splice(msgsList.length - 1, 1, updatedMsg)
            return
        }

        msgsList.push(data)
        lastMsgUserId = data.sender_id;        
    })

    return(
        msgsList?.map((openChatMsg, index)=>{
            return userData?.userId === openChatMsg.sender_id ? (
                <LocalMsgDisplay 
                key={`${index}-${openChatMsg.sender_id}`}
                msg={openChatMsg.msg}
                name={openChatMsg.sender_name}
                extraMsg={openChatMsg.extraMsg}/>
            ) : (
                <RemoteMsgDisplay 
                key={`${index}-${openChatMsg.sender_id}`}
                msg={openChatMsg.msg}
                name={openChatMsg.sender_name}
                extraMsg={openChatMsg.extraMsg}/> 
            )
        })
    )
}