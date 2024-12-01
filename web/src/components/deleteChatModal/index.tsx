import { useState } from "react";
import classes from "../../lib/classes";
import Button from "../button";
import CenteredModalContainer from "../centeredModalContainer";
import { deleteOpenChat } from "../../api/actions/chat_actions";
import { defaultAppState } from "../../lib/constant";
import { toast } from "react-toastify";
import { deleteUserOpenChat } from "../../lib/functions";


export default function DeleteChatModal(
    { closeModal, showModal, isOwner, chatId, userId, performAfterDeletion } : 
    { 
        showModal: boolean, 
        closeModal: () => void, 
        isOwner: boolean, 
        chatId: string, 
        userId: string,
        performAfterDeletion?: () => void
    }
){
    const [deletingChat, setDeletingChat] = useState(false);

    function deleteChat(){
        setDeletingChat(true);
        if(isOwner){
            deleteOpenChat(chatId, userId)
            .then((resp)=>{
                setDeletingChat(false);
                const {reqState} = resp;
                deleteUserOpenChat(chatId);
                closeModal();
                if(reqState === defaultAppState.success){
                    toast.success('Chat deleted Successfully');
                    performAfterDeletion && performAfterDeletion();
                }
            })
        }else{
            setDeletingChat(false);
            deleteUserOpenChat(chatId);
            closeModal();
        }
    }

    return(
        <CenteredModalContainer
        closeModal={closeModal}
        showModal={showModal}>
            <div className="bg-white rounded-lg p-4">
                <h1 className="text-lg mb-5 font-bold ">Delete Chat</h1>
                {isOwner ? 
                <p className="text-center text-red-500">
                    Are you sure you want to delete the chat? <br />
                    This will delete all data and completly delete the chat!
                </p> :
                <p>
                    Are you sure you want to delete the chat? <br />
                </p>}

                <div className="flex justify-between mt-5">
                    <button className={classes.btn.outlined}
                    onClick={closeModal}>
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
    )
}