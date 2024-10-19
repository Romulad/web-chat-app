import { useEffect, useState } from "react";
import classes from "../../../lib/classes";
import { connectedOpenChatUserRespData, openChatRespDataScheme } from "../../../lib/definitions";
import { getUserOpenChatInfo, parseSocketData } from "../../../lib/functions";
import { toast } from "react-toastify";

import ConnectedUserModal from "./connectedUserModal";
import { openChatConnectionMsgType } from "../../../lib/constant";
import UserRequestsModal from "./userRequestsModal";



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


    useEffect(()=>{
        ws?.addEventListener('message', (ev)=>{
            const data = parseSocketData(ev.data);
            if(
                data.type === openChatConnectionMsgType.request_join
            ){
                setUserRequests([...userRequests, data]);
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

    return(
        <>
        <div className="max-w-[900px] min-[910px]:mx-auto mx-3 pb-5 pt-5 flex flex-col gap-5 h-screen">
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

            <div className="grow flex flex-col justify-between overflow-auto gap-3 pb-3 px-3">
                <div className="grow overflow-y-auto overflow-x-hidden">
                </div>

                <div className="w-full flex items-center gap-3">
                    <input type="text" 
                    placeholder="Type a message and click send"
                    className="w-full block p-4 bg-slate-100 rounded-full grow"/>
                    <button className={classes.btn.blue}>
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