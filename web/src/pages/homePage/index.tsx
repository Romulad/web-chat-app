import { useState } from "react";
import { motion } from "motion/react";

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
        <div className="text-lg landing-page-bg bg-gray-100 grid h-screen overflow-hidden items-center justify-center">
            <div>
                <motion.button 
                className={`${classes.btn.green} shadow-lg`}
                onClick={toggleNewChatModal}
                initial={{ y: 0 }}
                animate={{ y: [0, -30, 0] }}
                transition={{
                    duration: 4, 
                    repeat: Infinity, 
                    repeatType: "loop",
                    ease: "easeInOut"
                }}>
                    Start a new chat
                </motion.button>
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