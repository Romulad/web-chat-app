import { useState } from "react";

import { getUseropenChatData } from "../../lib/functions";
import LabelInput from "../labelInput.tsx";
import { Link } from "react-router-dom";
import { getOpenChatPath } from "../../lib/paths.ts";
import { useChatDataContextValue } from "../../context/chatDataContext.tsx";


export default function OpenChatSideBar(){
    const { chatId } = useChatDataContextValue()
    const userOpenChats = getUseropenChatData();
    const [searchStr, setSearchStr] = useState("");

    return(
        chatId &&
        <div className="p-4 border-r-2 overflow-auto relative">
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
    )
}