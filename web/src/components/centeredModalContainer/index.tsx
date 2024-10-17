import React from "react";
import Overlay from "../overlay";


export default function CenteredModalContainer(
    { 
        children,
        closeModal,
        showModal
    } : { 
        showModal: boolean,
        closeModal: () => void,
        children: React.ReactNode 
    }
){
    return(
        <>
        <Overlay 
        onOverlayClick={closeModal}
        showOverlay={showModal}/>

        <div className={`w-full min-[550px]:w-[500px] fixed bg-transparent rounded-lg top-1/2 left-1/2 z-[1000]
        -translate-x-1/2 -translate-y-1/2 ${showModal ? "" : "hidden"}`}>
            {children}
        </div>
        </>
    )
}