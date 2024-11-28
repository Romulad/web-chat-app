import { useNavigate } from "react-router-dom";

import classes from "../../lib/classes";
import CenteredModalContainer from "../centeredModalContainer";
import LabelInput from "../labelInput.tsx";
import { getOpenChatPath } from "../../lib/paths.ts";
import { useState } from "react";


export default function JoinNewChatModal(
    { showNewChatModal, closeModal } : { showNewChatModal: boolean; closeModal: () => void }
){
    const navigate = useNavigate();
    const [chatId, setChatId] = useState("");

    function onJoinBtnClick(){
        chatId && navigate(getOpenChatPath(chatId))
    }

    return(
        <CenteredModalContainer
        closeModal={closeModal}
        showModal={showNewChatModal}
        >
            <div className="bg-white p-4 rounded-lg ">
                <h1 className="font-semibold text-lg mb-6">
                    Join a new chat
                </h1>

                <LabelInput
                label="Chat code: "
                name="chat-id"
                placeholder="Enter the chat code/id"
                required
                value={chatId}
                onChange={(ev)=>{setChatId(ev.target.value)}}/>

                <div className="flex justify-end mt-3">
                    <button className={`${classes.btn.green}`} onClick={onJoinBtnClick}>
                        Join chat
                    </button>
                </div>
            </div>
        </CenteredModalContainer>
    )
}