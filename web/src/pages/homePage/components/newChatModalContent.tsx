import { useState } from "react";
import { LabelInput } from "../../../components";
import classes from "../../../lib/classes";


export default function NewChatModalContent(
    {toggleNewChatModal} : {toggleNewChatModal: (()=>void)}
){
    const [showLinkView, setShowLinkView] = useState(false);

    function toggleLinkView(){
        setShowLinkView(!showLinkView)
    }

    return(
        <>
        <h1 className="text-xl font-medium mb-4">Start a new chat</h1>

        <LabelInput 
        label="Your name:"
        name="name"
        placeholder="Enter your name"/>

        <div className="flex justify-between mt-4 flex-wrap gap-3">
            <button className={classes.btn.outlined} onClick={toggleNewChatModal}>
                Cancel
            </button>

            <button className={classes.btn.blue}
            onClick={toggleLinkView}>
                Get chat link
            </button>
        </div>
        </>
    )
}