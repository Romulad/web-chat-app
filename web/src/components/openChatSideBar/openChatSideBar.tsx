import { useState } from "react";

import { getUseropenChatData } from "../../lib/functions";
import LabelInput from "../labelInput.tsx";


export default function OpenChatSideBar(
    { currentChatId } : { currentChatId: string }
){
    const userOpenChats = getUseropenChatData();
    const [searchStr, setSearchStr] = useState("");

    return(
        <>
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
                    <li key={chatData.chatId} className="mb-2">
                        <button className={`duration-500 w-full flex items-center gap-3 rounded-lg hover:bg-slate-50 p-2 ${currentChatId == chatData.chatId ? "text-white shadow-lg bg-green-500 hover:bg-green-500" : ""}`}>
                            <div className="bg-slate-100 text-black py-2 px-3 rounded-full">{chatData.chatName.charAt(0)}</div>
                            <div className="flex flex-col gap-1 items-start">
                                <span className="font-semi-bold">{chatData.chatName}</span>
                                <span className={`${currentChatId == chatData.chatId ? "text-white" : "text-gray-600"}`}>Last message</span>
                            </div>
                        </button>
                    </li>
                ))}
            </ul> :
            <div className="flex items-center h-[90%] justify-center text-center">
                No chat yet? Start by inviting someone or add a friend
            </div>}
        </div>
        </>
    )
}