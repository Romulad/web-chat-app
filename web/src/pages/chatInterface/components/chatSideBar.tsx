import { useEffect, useState } from "react";

import { UserChatHistoryResp } from "../../../lib/definitions"
import { fetchUserChatHistories } from "../../../api/actions/auth"
import { defaultAppState } from "../../../lib/constant"
import classes from "../../../lib/classes"
import FindInviteNewUserModal from "./findInviteUserModal";



export default function ChatSideBar(){
    const [userChatHistories, setUserChatHistories] = useState<UserChatHistoryResp>();
    const [showInvitationModal, SetShowInvitationModal] = useState(false);


    useEffect(()=>{
        fetchUserChatHistories()
        .then((resp)=>{
            if(resp.reqState === defaultAppState.success){
                setUserChatHistories(resp.respData)
            }
        })
    }, [])

    function toggleInvitationModal(){
        SetShowInvitationModal(!showInvitationModal)
    }

    return(
        <>
        <div className="p-4 border-r-2 overflow-auto">
            <button className={classes.btn.blue}
            onClick={toggleInvitationModal}>
                Find user to chat with
            </button>

            {userChatHistories?.length ?
            <div></div> :
            <div className="flex items-center h-[90%] justify-center text-center">
                No chat yet? Start by inviting someone or add a friend
            </div>}
        </div>
        
        <FindInviteNewUserModal 
        closeModal={toggleInvitationModal}
        showModal={showInvitationModal}/>
        </>
    )
}