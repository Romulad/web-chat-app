import { useState } from "react";
import { useParams } from "react-router-dom";

import { 
    generateUserId, 
    getUserOpenChatInfo, 
    setUserOpenChatInfo, 
    validateNameInput 
} from "../../lib/functions";
import { CenteredModalContainer, LabelInput } from "../../components";
import classes from "../../lib/classes";
import OpenChatConnectionManager from "./components/openChatConnectionManager";


export default function OpenChatChatPage(){
    const { chatId } = useParams();
    const userInfo = getUserOpenChatInfo();
    const [userData, setUserData] = useState(userInfo)
    const [name, setName] = useState('');
    const [nameError, setNameError] = useState('');

    function onSaveNameBtnClick(){
        setNameError('');

        const result = validateNameInput(name);
        if (typeof result === "string"){
            setNameError(result)
            return
        }
        const data = setUserOpenChatInfo({name, userId: generateUserId(name)});
        setUserData(data);
    }

    return(
        userData ? (
            <>
            <OpenChatConnectionManager 
            userData={userData}
            chatId={chatId || ""}/>
            </>
        ) : (
            <CenteredModalContainer closeModal={()=>{}} showModal={true}>
                <div className="bg-white p-4 rounded-lg ">
                    <LabelInput 
                    label="Name:"
                    name="name"
                    type="text"
                    placeholder="Enter your name"
                    value={name}
                    onChange={(ev)=>{setName(ev.target.value)}}
                    inputError={nameError}/>
                    
                    <div className="flex justify-end mt-5">
                        <button className={classes.btn.blue}
                        onClick={onSaveNameBtnClick}>
                            Save
                        </button>
                    </div>
                </div>
            </CenteredModalContainer>
        )
    )
}