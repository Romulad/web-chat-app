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
    const [reqData, setReqData] = useState({
        ownerName: userInfo?.name || "",
        chatName: "",
    });
    const [inputError, setInputError] = useState({
        chatNameError: "",
        ownerNameError: ""
    });
    const [creatingChat, setCreatingChat] = useState(false);

    function toggleLinkView(){
        setShowLinkView(!showLinkView)
    }

    function getUserChatIds(){
        return {
            chatId: generateChatId(),
            initiatorId: userInfo ? userInfo.userId : generateUserId(reqData.ownerName)
        }
    }

    async function onGetLinkBtnClick(){
        setInputError({ownerNameError: "", chatNameError: ""});
        
        if(!reqData.ownerName){
            setInputError((errors)=>({...errors, ownerNameError: 'Please enter a valid name'}))
            return
        }

        if(reqData.ownerName.length < 3){
            setInputError((errors)=>({...errors, ownerNameError: 'Minimum 3 characters'}))
            return
        }

        if(reqData.chatName.length < 3){
            setInputError((errors)=>({...errors, chatNameError: 'Minimum 3 characters'}))
            return
        }

        const userChatIds = getUserChatIds();
        if(reqData.ownerName !== userInfo?.name)
            setUserOpenChatInfo({name: reqData.ownerName, userId: userChatIds.initiatorId});

        setCreatingChat(true);
        const {reqState, respData} = await createNewOpenChat(
            userChatIds.chatId, userChatIds.initiatorId, reqData.ownerName, reqData.chatName
        );
        setCreatingChat(false);

        if(reqState === defaultAppState.success){
            updateUseropenChatData(respData?.chat_id, reqData.chatName, respData.initiation_date);
            setChatLink(getOpenChatPath(userChatIds.chatId));
            toggleLinkView();
        }
    }

    const nameView = (
        <>
        <LabelInput 
        label="Your name:"
        name="name"
        placeholder="Enter your name"
        inputError={inputError.ownerNameError}
        value={reqData.ownerName}
        onChange={(ev)=> setReqData((data)=>({...data, ownerName: ev.target.value}))}/>

        <LabelInput 
        label="Give a name to your chat:"
        name="chat-name"
        placeholder="Chat name"
        minLength={3}
        inputError={inputError.chatNameError}
        value={reqData.chatName}
        onChange={(ev)=> setReqData((data)=>({...data, chatName: ev.target.value}))}/>

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