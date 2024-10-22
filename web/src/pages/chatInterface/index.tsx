import { useEffect } from "react"
import { fetchAboutUserData } from "../../api/actions/auth";
import { defaultAppState } from "../../lib/constant";
import ChatSideBar from "./components/chatSideBar";


export default function ChatInterface(){
    
    useEffect(()=>{
        fetchAboutUserData()
        .then((resp)=>{
            if(resp.reqState === defaultAppState.success){

            }
        });

    }, [])

    return(
        <div className="grid grid-cols-[250px_1fr] w-screen h-screen overflow-auto">
            <ChatSideBar />

            <div className="p-4 overflow-auto">
                <div className="flex h-full items-center justify-center">
                    Click on a chat to view messages and start chatting
                </div>
            </div>
        </div>
    )
}