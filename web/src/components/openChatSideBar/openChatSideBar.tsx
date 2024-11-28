import { useState } from "react";

import { getUseropenChatData } from "../../lib/functions";
import LabelInput from "../labelInput.tsx";
import { Link } from "react-router-dom";
import { getOpenChatPath, openChatHomePath } from "../../lib/paths.ts";
import { useChatDataContextValue } from "../../context/chatDataContext.tsx";
import classes from "../../lib/classes.ts";
import JoinNewChatModal from "../joinNewChatModal/index.tsx";
import { useMobileUiContext } from "../../context/mobileUiStateContext.tsx";


export default function OpenChatSideBar(){
    const { chatId } = useChatDataContextValue()
    const { showChatInterface, toggleChartInterface } = useMobileUiContext();
    const userOpenChats = getUseropenChatData();
    const [searchStr, setSearchStr] = useState("");
    const [showNewChatModal, setShowNewChatModal] = useState(false);

    function toggleNewChatModal(){
        setShowNewChatModal(!showNewChatModal)
    }

    return(
        <>
        <div className={`${showChatInterface ? "hidden" : "block"} md:block p-4 border-l-2 md:border-l-0 border-r-2 overflow-auto relative max-w-[300px] mx-auto md:mx-0`}>
            <div className="flex justify-between items-center gap-2 mb-5">
                <Link to={openChatHomePath}
                className={`${classes.btn.outlined}`}
                >
                    All chats
                </Link>
                <button className={`${classes.btn.blue}`} onClick={toggleNewChatModal}>
                    New chat +
                </button>
            </div>

            <div className="sticky top-0 bg-white">
                <LabelInput 
                type="search"
                label=""
                name="chat"
                placeholder="Search by chat id or name"
                value={searchStr}
                onChange={(ev)=>{setSearchStr(ev.target.value.toLowerCase())}}/>
            </div>

            {userOpenChats?.length ?
            <ul className="mt-8">
                {userOpenChats
                .filter((data) => (
                    data.chatId.toLowerCase().includes(searchStr) || 
                    data.chatName.toLowerCase().includes(searchStr)
                ))
                .map((chatData)=>(
                    <li key={chatData.chatId} className="mb-5">
                        <Link to={getOpenChatPath(chatData?.chatId)}
                        onClick={()=>{
                            if(chatId == chatData.chatId){
                                toggleChartInterface();
                            }
                        }}
                        className={`duration-500 w-full flex items-center gap-3 rounded-lg hover:bg-slate-50 p-3 ${chatId == chatData.chatId ? "shadow-xl bg-slate-50 hover:bg-slate-50" : ""}`}>
                            <div className="bg-slate-200 text-black py-2 px-3 rounded-full">{chatData?.chatName?.charAt(0)}</div>
                            <div className="flex flex-col gap-1 items-start">
                                <span className="font-semi-bold">{chatData.chatName}</span>
                                <span className={"text-gray-600 text-sm"}>
                                    {chatData.chatId.slice(0, 25) + " ..."}
                                </span>
                            </div>
                        </Link>
                    </li>
                ))}
            </ul> :
            <div className="mt-10 text-center">
                No chat yet
            </div>}
        </div>
        <JoinNewChatModal 
        closeModal={toggleNewChatModal}
        showNewChatModal={showNewChatModal}
        />
        </>
    )
}