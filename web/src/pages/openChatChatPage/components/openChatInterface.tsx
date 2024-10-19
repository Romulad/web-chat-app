import React, { useEffect, useRef, useState } from "react";
import classes from "../../../lib/classes";
import { connectedOpenChatUserRespData, OpenChatMsg, openChatReqDataScheme, openChatRespDataScheme } from "../../../lib/definitions";
import { getUserOpenChatInfo, parseSocketData } from "../../../lib/functions";
import { toast } from "react-toastify";

import ConnectedUserModal from "./connectedUserModal";
import { openChatConnectionMsgType } from "../../../lib/constant";
import UserRequestsModal from "./userRequestsModal";
import { LocalMsgDisplay, RemoteMsgDisplay } from "../../../components";



export default function OpenChatInterface(
    {
        chatUsers, 
        ws,
        chatId
    } : {
        chatUsers: Array<connectedOpenChatUserRespData>,
        ws: WebSocket | undefined,
        chatId: string,
    }
){
    const [showUserListModal, setShowUserListModal] = useState(false);
    const [showUserRequestsModal, setShowUserRequestsModal] = useState(false);
    const [userRequests, setUserRequests] = useState<Array<openChatRespDataScheme>>([]);
    const userData = getUserOpenChatInfo();
    const [innerChatUsers, setInnerChatUser] = useState<Array<connectedOpenChatUserRespData>>(chatUsers);
    const [openChatMsgs, setOpenChatMsgs] = useState<Array<OpenChatMsg>>([]);
    const [msg, setMsg] = useState('');
    const msgContainerRef = useRef<HTMLDivElement>(null);

    useEffect(()=>{
        ws?.addEventListener('message', (ev)=>{
            const data = parseSocketData(ev.data);
            if(
                data.type === openChatConnectionMsgType.request_join
            ){
                setUserRequests((userRequests)=> [...userRequests, data]);
                toast.info(`${data.user_name} is asking to join the chat`);
            }else if(
                data?.type === openChatConnectionMsgType.notify_new_user
            ){
                if(data.chat_users){
                    toast.info(`${data.user_name} join the chat`);
                    setInnerChatUser(data.chat_users);
                }
            }else if(
                data?.type === openChatConnectionMsgType.user_disconnect
            ){
                toast.info(`${data.user_name} leave the chat`);
                setInnerChatUser(innerChatUsers.filter((user)=> user.user_id !== data.user_id));
            }else if(
                data?.type === openChatConnectionMsgType.new_message
            ){
                const msgData : OpenChatMsg = {
                    name: data.user_name || "",
                    text: typeof data.data === "string" && data.data || "",
                    userId: data.user_id || "",
                }
                setOpenChatMsgs((msgs)=> [...msgs, msgData]);
                showContainerLastMsg()
            }
        })

    }, [])


    function toggleUserListModal(){
        setShowUserListModal(!showUserListModal);
    }

    function toggleUserRequestModal(){
        setShowUserRequestsModal(!showUserRequestsModal);
    }

    function isAdmin(userId: string){
        const chatUser = innerChatUsers.find((chatUser)=> chatUser.user_id === userId);
        return chatUser?.is_owner
    }

    function sendMsg(){
        const msgData: openChatReqDataScheme = {
            chat_id: chatId,
            data: msg,
            type: openChatConnectionMsgType.new_message,
            user_id: userData?.userId || "",
            user_name: userData?.name || "",
        }
        ws?.send(JSON.stringify(msgData));

        const newMsg : OpenChatMsg = {
            name: userData?.name || "", 
            text: msg,
            userId: userData?.userId || ""
        }
        setOpenChatMsgs([...openChatMsgs, newMsg])
    }

    function showContainerLastMsg(){
        setTimeout(() => {
            msgContainerRef.current?.scrollTo(0, msgContainerRef.current?.scrollHeight)
        }, 5);
    }

    function onSendBtnClick(ev: React.MouseEvent){
        ev.preventDefault();
        if(!msg){
            return
        }

        sendMsg();
        setMsg('');
        showContainerLastMsg()
    }

    return(
        <>
        <div className="max-w-[900px] min-[910px]:mx-auto mx-3 pt-5 flex flex-col gap-5 h-screen">
            <div className="flex justify-between items-center px-4 py-3 bg-slate-50 shadow-lg rounded-lg ">
                <button className=" flex flex-col"
                onClick={toggleUserListModal}>
                    <p className="sm:text-lg">
                        {chatId}
                    </p>
                    <p className="text-start text-sm text-gray-600">
                        <b>connected users:</b> {innerChatUsers.length}
                    </p>
                </button>

                {isAdmin(userData?.userId || "") && 
                <button className="relative"
                onClick={toggleUserRequestModal}>
                    <div className={`border-2 px-2 py-1 rounded-full ${userRequests.length ? "border-red-500" : ""}`}>
                        {userRequests.length}
                    </div>
                </button>}
            </div>

            <div className="grow flex flex-col justify-between overflow-auto gap-3 pb-4 px-3">
                <div className="grow overflow-y-auto overflow-x-hidden flex flex-col gap-2 pe-3"
                ref={msgContainerRef}>
                    {openChatMsgs?.map((openChatMsg)=>{
                        return userData?.userId === openChatMsg.userId ? (
                            <LocalMsgDisplay 
                            msg={openChatMsg.text}
                            name={openChatMsg.name}/>
                        ) : (
                            <RemoteMsgDisplay 
                            msg={openChatMsg.text}
                            name={openChatMsg.name}/> 
                        )
                    })}
                </div>

                <div className="w-full flex items-center gap-3">
                    <input type="text" 
                    placeholder="Type a message and click send"
                    className="w-full block p-4 bg-slate-100 rounded-full grow"
                    value={msg} onChange={(ev)=>{setMsg(ev.target.value)}}/>
                    <button className={classes.btn.blue}
                    onClick={onSendBtnClick} disabled={msg.length <= 0}>
                        Send
                    </button>
                </div>
            </div>
        </div>
        
        <ConnectedUserModal 
        chatUsers={innerChatUsers}
        showUserListModal={showUserListModal}
        toggleUserListModal={toggleUserListModal}/>

        <UserRequestsModal 
        showUserRequestsModal={showUserRequestsModal}
        toggleUserRequestsModal={toggleUserRequestModal}
        userRequests={userRequests}
        ws={ws}
        setUserRequests={setUserRequests}/>
        </>
    )
}