import React, { useEffect, useRef, useState } from "react";
import { toast } from "react-toastify";

import classes from "../../../lib/classes";
import { 
    OpenChatMsg, 
    openChatReqDataScheme, 
    openChatRespDataScheme 
} from "../../../lib/definitions";
import { 
    deleteUserOpenChat, 
    getChatData, 
    getUserOpenChatInfo, 
    parseSocketData 
} from "../../../lib/functions";
import ConnectedUserModal from "./connectedUserModal";
import { openChatConnectionMsgType } from "../../../lib/constant";
import UserRequestsModal from "./userRequestsModal";
import { DeleteChatModal, OpenChatMessageDisplay, ThreeHorizontalDash, TrashIcon } from "../../../components";
import { useNavigate } from "react-router-dom";
import { openChatHomePath } from "../../../lib/paths";
import { useChatDataContextValue } from "../../../context/chatDataContext";
import { useMobileUiContext } from "../../../context/mobileUiStateContext";


export default function OpenChatInterface(
    { ws } : { ws: WebSocket | undefined }
){
    const { chatId, fullChatData } = useChatDataContextValue();
    const { toggleChartInterface, showChatInterface } = useMobileUiContext();

    const isChatOwner = getChatData(chatId)?.isOwner;
    const userData = getUserOpenChatInfo();
    const navigate = useNavigate();

    const [userRequests, setUserRequests] = useState<Array<openChatRespDataScheme>>([]);
    const [innerChatUsers, setInnerChatUsers] = useState(fullChatData?.chat_users || []);
    const [activeUsersIds, setActiveUsersIds] = useState(fullChatData?.connected_users || []);
    const [openChatMsgs, setOpenChatMsgs] = useState(fullChatData?.chat_msgs || []);

    const [msg, setMsg] = useState('');

    const [showUserListModal, setShowUserListModal] = useState(false);
    const [showUserRequestsModal, setShowUserRequestsModal] = useState(false);
    const [showDeleteChatModal, setShowDeleteChatModal] = useState(false);
    const msgContainerRef = useRef<HTMLDivElement>(null);

    useEffect(()=>{
        ws?.addEventListener('message', (ev)=>{
            const data = parseSocketData(ev.data);
            if(
                data.type === openChatConnectionMsgType.request_join
            ){
                setUserRequests((userRequests) => {
                    const existed = userRequests.find((request)=> request.user_id === data.user_id)
                    if(existed){
                        return userRequests
                    }else{
                        return [...userRequests, data]
                    }
                });
                if(data.chat_id === chatId){
                    toast.info(`${data.user_name} is asking to join the chat`);
                }else{
                    const chatData = getChatData(data.chat_id);
                    toast.info(`${data.user_name} is asking to join ${chatData?.chatName || ""}`);
                }
            }
            
            else if(
                data?.type === openChatConnectionMsgType.notify_new_user
            ){
                if(data.chat_id === chatId)
                    toast.info(`${data.user_name} join the chat`);
                    setInnerChatUsers(data.chat_users || []);
                    setActiveUsersIds(data.connected_users || [])
            }
            
            else if(
                data?.type === openChatConnectionMsgType.user_disconnect
            ){
                toast.info(`${data.user_name} leave the chat`);
                // update connected user ids
                if(data.user_id && activeUsersIds?.includes(data.user_id)){
                    setActiveUsersIds(
                        activeUsersIds?.filter((userId)=> userId !== data.user_id)
                    );
                }
            }
            
            else if(
                data?.type === openChatConnectionMsgType.new_message
            ){
                if(data.user_name && data.data && data.user_id && data.send_at){
                    const msgData : OpenChatMsg = {
                        sender_name: data.user_name,
                        msg: typeof data.data === "string" && data.data || "",
                        sender_id: data.user_id,
                        chat_id: data.chat_id,
                        send_at: data.send_at
                    }
                    setOpenChatMsgs((messages) => [...messages, msgData]);
                    showContainerLastMsg();
                }
            }
            
            else if(
                data?.type === openChatConnectionMsgType.chat_deleted
            ){
                if(!isChatOwner) toast.info(`Chat have been deleted`);
                setTimeout(() => {
                    performAfterChatDeletion()
                }, 1000);
            }
        });

        showContainerLastMsg();

    }, [])


    function toggleUserListModal(){
        setShowUserListModal(!showUserListModal);
    }

    function toggleUserRequestModal(){
        setShowUserRequestsModal(!showUserRequestsModal);
    }

    function toggleDeleteChatModal(){
        setShowDeleteChatModal(!showDeleteChatModal);
    }

    function isAdmin(userId: string){
        const chatUser = innerChatUsers?.find((chatUser)=> chatUser.user_id === userId);
        return chatUser?.is_owner
    }

    function performAfterChatDeletion(){
        deleteUserOpenChat(chatId);
        navigate(openChatHomePath);
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

        const date = new Date()
        const newMsg : OpenChatMsg = {
            sender_name: userData?.name || "",
            msg: msg,
            sender_id: userData?.userId || "",
            chat_id: chatId,
            send_at: date.toUTCString()
        }
        setOpenChatMsgs([...(openChatMsgs || []), newMsg]);
    }

    function showContainerLastMsg(){
        setTimeout(() => {
            msgContainerRef.current?.scrollTo(0, msgContainerRef.current?.scrollHeight)
        }, 5);
    }

    function onSendBtnClick(ev: React.MouseEvent | React.FormEvent){
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
        <div className={`${showChatInterface ? "flex" : "hidden"} md:flex flex-col gap-5 h-screen`}>
            <div className="flex justify-between items-center px-4 py-3 shadow ">
                <button className=" flex flex-col"
                onClick={toggleUserListModal}>
                    <p className="sm:text-lg">
                        {chatId.slice(0, 15) + "..."}
                    </p>
                    <p className="text-start text-sm text-gray-600">
                        <b>connected:</b> {activeUsersIds?.length || 0}
                    </p>
                </button>

                <div className="flex gap-2 items-center">
                    <button onClick={toggleChartInterface} className="md:hidden">
                        <ThreeHorizontalDash 
                        className="size-6"/>
                    </button>

                    {isAdmin(userData?.userId || "") &&
                    <div className="flex items-center gap-3">
                        <button className="relative"
                        onClick={toggleUserRequestModal}>
                            <div className={`border-2 px-2 py-1 rounded-full ${userRequests.length ? "border-red-500" : ""}`}>
                                {userRequests.length}
                            </div>
                        </button>

                        <button onClick={toggleDeleteChatModal}>
                            <TrashIcon 
                            className="size-6 text-red-500"/>
                        </button>
                    </div>}
                </div>
            </div>

            <div className="grow flex flex-col justify-between overflow-auto gap-3 pb-6 px-3">
                <div className="grow overflow-y-auto overflow-x-hidden "
                ref={msgContainerRef}>
                    <div className="xl:w-3/4 mx-auto flex flex-col gap-2 pe-3">
                        <OpenChatMessageDisplay 
                        openChatMsgs={openChatMsgs}/>
                    </div>
                </div>

                <form className="w-[95%] md:w-5/6 lg:w-3/4 2xl:w-1/2 mx-auto flex items-center gap-3"
                onSubmit={onSendBtnClick}>
                    <input type="text" 
                    placeholder="Type a message and click send"
                    className="w-full block p-4 bg-slate-100 rounded-full grow"
                    value={msg} onChange={(ev)=>{setMsg(ev.target.value)}}/>
                    <button className={classes.btn.blue}
                    onClick={onSendBtnClick} disabled={msg.length <= 0}>
                        Send
                    </button>
                </form>
            </div>
        </div>
        
        <ConnectedUserModal 
        chatUsers={innerChatUsers || []}
        connectedIds={activeUsersIds || []}
        showUserListModal={showUserListModal}
        toggleUserListModal={toggleUserListModal}/>

        <UserRequestsModal
        showUserRequestsModal={showUserRequestsModal}
        toggleUserRequestsModal={toggleUserRequestModal}
        userRequests={userRequests}
        ws={ws}
        setUserRequests={setUserRequests}/>

        <DeleteChatModal 
        chatId={chatId}
        closeModal={toggleDeleteChatModal}
        isOwner={getChatData(chatId)?.isOwner || false}
        showModal={showDeleteChatModal}
        userId={userData?.userId || ""}
        performAfterDeletion={performAfterChatDeletion}
        />
        </>
    )
}