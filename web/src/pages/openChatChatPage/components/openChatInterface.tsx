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
import { defaultAppState, openChatConnectionMsgType } from "../../../lib/constant";
import UserRequestsModal from "./userRequestsModal";
import { Button, CenteredModalContainer, OpenChatMessageDisplay, TrashIcon } from "../../../components";
import { deleteOpenChat } from "../../../api/actions/chat_actions";
import { useNavigate } from "react-router-dom";
import { openChatHomePath } from "../../../lib/paths";
import { useChatDataContextValue } from "../../../context/chatDataContext";


export default function OpenChatInterface(
    { ws } : { ws: WebSocket | undefined }
){
    const { chatId, fullChatData } = useChatDataContextValue()

    const isChatOwner = getChatData(chatId)?.isOwner;
    const userData = getUserOpenChatInfo();
    const navigate = useNavigate();

    const [userRequests, setUserRequests] = useState<Array<openChatRespDataScheme>>([]);
    const [innerChatUsers, setInnerChatUsers] = useState(fullChatData?.chat_users || []);
    const [activeUsersIds, setActiveUsersIds] = useState(fullChatData?.connected_users || []);
    const [openChatMsgs, setOpenChatMsgs] = useState(fullChatData?.chat_msgs || []);

    const [msg, setMsg] = useState('');
    const [deletingChat, setDeletingChat] = useState(false);

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
        })
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

    function deleteChat(){
        setDeletingChat(true);
        deleteOpenChat(chatId, userData?.userId || "")
        .then((resp)=>{
            setDeletingChat(false);
            const {reqState} = resp;
            if(reqState === defaultAppState.success){
                toast.success('Chat deleted Successfully');
                performAfterChatDeletion()
            }
        })
    }

    return(
        <>
        <div className="flex flex-col gap-5 h-screen">
            <div className="flex justify-between items-center px-4 py-3 shadow ">
                <button className=" flex flex-col"
                onClick={toggleUserListModal}>
                    <p className="sm:text-lg">
                        {chatId}
                    </p>
                    <p className="text-start text-sm text-gray-600">
                        <b>connected users:</b> {activeUsersIds?.length || 0}
                    </p>
                </button>

                {isAdmin(userData?.userId || "") &&
                <div className="flex items-center gap-3">
                    <button onClick={toggleDeleteChatModal}>
                        <TrashIcon 
                        className="size-6 text-red-500"/>
                    </button>

                    <button className="relative"
                    onClick={toggleUserRequestModal}>
                        <div className={`border-2 px-2 py-1 rounded-full ${userRequests.length ? "border-red-500" : ""}`}>
                            {userRequests.length}
                        </div>
                    </button>
                </div>}
            </div>

            <div className="grow flex flex-col justify-between overflow-auto gap-3 pb-6 px-3">
                <div className="grow overflow-y-auto overflow-x-hidden flex flex-col gap-2 pe-3"
                ref={msgContainerRef}>
                    <OpenChatMessageDisplay 
                    openChatMsgs={openChatMsgs}/>
                </div>

                <form className="w-1/2 mx-auto flex items-center gap-3"
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

        <CenteredModalContainer
        closeModal={toggleDeleteChatModal}
        showModal={showDeleteChatModal}>
            <div className="bg-white rounded-lg p-4">
                <h1 className="text-lg mb-5 font-bold ">Delete Chat</h1>
                <p className="text-center">
                    Are you sure you want to delete the chat?
                </p>

                <div className="flex justify-between mt-5">
                    <button className={classes.btn.outlined}
                    onClick={toggleDeleteChatModal}>
                        Cancel
                    </button>
                    <Button 
                    className={classes.btn.red}
                    defaultText="Yes, delete"
                    isInAction={deletingChat}
                    isInActionText="Deleting"
                    onClick={deleteChat}/>
                </div>
            </div>
        </CenteredModalContainer>
        </>
    )
}