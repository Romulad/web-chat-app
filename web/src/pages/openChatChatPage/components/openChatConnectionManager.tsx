import { openChatUser } from "../../../lib/definitions";
import { getUserNotAllowedIds, getChatData } from "../../../lib/functions";
import ManageNewChatConection from "./manageNewChatConnection";
import NotAllowedChatMsg from "./notAllowedChatMsg";


export default function OpenChatConnectionManager(
    { userData, chatId }: { userData: openChatUser, chatId: string }
){
    const chatData = getChatData(chatId);
    const notAllowedChatIds = getUserNotAllowedIds();

    return(
        notAllowedChatIds.includes(chatId) ? (
            <NotAllowedChatMsg 
            userId={userData.userId}/>
        ) : chatData ? (
            <div></div>
        ) : (
            <ManageNewChatConection 
            chatId={chatId}
            userData={userData}/>
        )
    )
}