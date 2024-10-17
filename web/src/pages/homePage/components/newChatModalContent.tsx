import { useState } from "react";
import { Link } from "react-router-dom";

import { LabelInput } from "../../../components";
import classes from "../../../lib/classes";
import { createNewOpenChat } from "../../../api/actions/chat_actions";
import { defaultAppState } from "../../../lib/constant";
import { 
    generateChatId, 
    generateUserId, 
    getUserOpenChatInfo, 
    setUserOpenChatInfo, 
    updateUseropenChatData 
} from "../../../lib/functions";
import { getOpenChatPath } from "../../../lib/paths";


export default function NewChatModalContent(
    {toggleNewChatModal} : {toggleNewChatModal: (()=>void)}
){
    const userInfo = getUserOpenChatInfo();
    const [showLinkView, setShowLinkView] = useState(false);
    const [chatLink, setChatLink] = useState('');
    const [ownerName, setOwnerName] = useState<string>(userInfo?.name || "");
    const [inputError, setInputError] = useState<string>("");
    const [creatingChat, setCreatingChat] = useState(false);

    function toggleLinkView(){
        setShowLinkView(!showLinkView)
    }

    function getUserChatIds(){
        return {
            chatId: generateChatId(),
            initiatorId: userInfo ? userInfo.userId : generateUserId(ownerName)
        }
    }

    async function onGetLinkBtnClick(){
        setInputError('');
        
        if(!ownerName){
            setInputError('Please enter a valid name')
            return
        }

        if(ownerName.length < 3){
            setInputError('Minimum 3 characters')
            return
        }

        const idsData = getUserChatIds();
        if(ownerName !== userInfo?.name)
            setUserOpenChatInfo({name: ownerName, userId: idsData.initiatorId});

        setCreatingChat(true);
        const {reqState, respData} = await createNewOpenChat(
            idsData.chatId, idsData.initiatorId, ownerName
        );
        setCreatingChat(false);

        if(reqState === defaultAppState.success){
            updateUseropenChatData(respData?.chat_id);
            setChatLink(getOpenChatPath(idsData.chatId));
            toggleLinkView();
        }
    }

    const nameView = (
        <>
        <LabelInput 
        label="Your name:"
        name="name"
        placeholder="Enter your name"
        inputError={inputError}
        value={ownerName}
        onChange={(ev)=>setOwnerName(ev.target.value)}/>

        <div className="flex justify-between mt-4 flex-wrap gap-3">
            <button className={classes.btn.outlined} onClick={toggleNewChatModal}>
                Cancel
            </button>

            <button className={creatingChat ? classes.btn.disabled : classes.btn.blue}
            disabled={creatingChat}
            onClick={onGetLinkBtnClick}>
                {creatingChat ? "Creating chat..." : "Get chat link"}
            </button>
        </div>
        </>
    )

    const linkView = (
        <>
        <LabelInput 
        label="Share this link to invite others to join:"
        name="chat-link"
        value={location.host + chatLink}
        readOnly/>

        <div className="flex justify-between mt-4 flex-wrap gap-3">
            <button className={classes.btn.outlined} onClick={toggleNewChatModal}>
                Cancel
            </button>

            <Link to={chatLink}
            className={classes.btn.green}>
                Open chat
            </Link>
        </div>
        </>
    )

    return(
        <>
        <h1 className="text-xl font-medium mb-4">
            Start a new chat
        </h1>
        {showLinkView ? linkView : nameView}
        </>
    )
}