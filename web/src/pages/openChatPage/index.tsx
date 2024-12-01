import { Link } from "react-router-dom";
import { getChatData, getUseropenChatData, getUserOpenChatInfo } from "../../lib/functions"
import { getOpenChatPath } from "../../lib/paths";
import { DeleteChatModal, TrashIcon } from "../../components";
import { useState } from "react";
import classes from "../../lib/classes";


export default function OpenChatPage(){
    const chatData = getUseropenChatData();
    const [chatId, setChatId] = useState("");
    const [showDeleteChatModal, setDeleteChatModal] = useState(false);

    function toggleDeleteChatModal(){
        setDeleteChatModal(!showDeleteChatModal)
    }

    return(
        <>
        <div className="h-screen overflow-hidden landing-page-bg bg-slate-100 flex items-center">
            <div className="w-full sm:w-[500px] sm:mx-auto mx-3 max-h-[500px] overflow-auto mt-10 bg-white shadow-lg rounded-lg p-4">
                {chatData && chatData.length ?(
                    <ul className="divide-y-2">
                {chatData?.map((data)=>(
                    <li key={data.chatId} className="py-3 flex items-center gap-2">
                        <Link to={getOpenChatPath(data.chatId)}
                        className="grow w-full flex flex-col gap-1 p-3 rounded-lg hover:bg-slate-100 ">
                            <span>
                                {data.chatName}
                            </span>
                            <span className="text-gray-600 text-sm">
                                {data.chatId.slice(0, 30) + "..."}
                            </span>
                        </Link>

                        <button
                        onClick={()=>{
                            toggleDeleteChatModal();
                            setChatId(data.chatId);
                        }}>
                            <TrashIcon 
                            className="size-6 text-red-500"
                            />
                        </button>
                    </li>
                ))}
                    </ul>
                ) : (
                    <div className={"flex justify-center"}>
                        <Link to={"/"} className={classes.btn.blue}>
                            Create a chat
                        </Link>
                    </div>
                )}
            </div>
        </div>

        {showDeleteChatModal &&
        <DeleteChatModal 
        chatId={chatId}
        closeModal={toggleDeleteChatModal}
        isOwner={getChatData(chatId)?.isOwner || false}
        showModal={showDeleteChatModal}
        userId={getUserOpenChatInfo()?.userId || ""}
        />}
        </>
    )
}