import { useState } from "react";

import { Overlay } from "../../components";
import classes from "../../lib/classes";
import NewChatModalContent from "./components/newChatModalContent";


export default function HomePage(){
    const [showNewChatModal, setShowNewChatModal] = useState<boolean>(false);

    function toggleNewChatModal(){
        setShowNewChatModal(!showNewChatModal)
    }

    return(
        <>
        <div className="h-screen overflow-hidden flex items-center justify-center">
            <div className="flex flex-wrap gap-3 justify-center">
                <button
                className={classes.btn.green} onClick={toggleNewChatModal}>
                    Start a new chat
                </button>
            </div>
        </div>

        <Overlay 
        onOverlayClick={toggleNewChatModal}
        showOverlay={showNewChatModal}/>

        <div className={`w-full min-[450px]:w-[400px] fixed bg-white rounded-lg p-4 top-1/2 left-1/2 z-[1000]
        -translate-x-1/2 -translate-y-1/2 ${showNewChatModal ? "" : "hidden"}`}>
            <NewChatModalContent 
            toggleNewChatModal={toggleNewChatModal}
            />
        </div>
        </>
    )
}