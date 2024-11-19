import { openChatUser } from "../../../lib/definitions";
import { getUserNotAllowedIds, getChatData } from "../../../lib/functions";
import { OpenChatSideBar } from "../../../components";
import ManageAddUserToChat from "./manageAddUserToChat";
import ManageNewChatConection from "./manageNewChatConnection";
import NotAllowedChatMsg from "./notAllowedChatMsg";


export default function OpenChatConnectionManager(
    { userData, chatId }: { userData: openChatUser, chatId: string }
){
    const chatData = getChatData(chatId);
    const notAllowedChatIds = getUserNotAllowedIds();

    return(
        <div className="grid grid-cols-[250px_1fr] w-screen h-screen overflow-auto">
            <OpenChatSideBar 
            currentChatId={chatId}/>

            {notAllowedChatIds.includes(chatId) ? (
                <NotAllowedChatMsg 
                userId={userData.userId}/>
            ) : 
            
            chatData ? (
                <ManageAddUserToChat 
                chatData={chatData}
                userData={userData}/>
            ) : 
            
            <ManageNewChatConection 
            chatId={chatId}
            userData={userData}/>}
        </div>
    )
}