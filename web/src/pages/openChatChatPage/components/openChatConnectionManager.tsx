import { 
    getUserNotAllowedIds, 
    getChatData, 
} from "../../../lib/functions";
import { OpenChatSideBar } from "../../../components";
import ManageAddUserToChat from "./manageAddUserToChat";
import ManageNewChatConection from "./manageNewChatConnection";
import NotAllowedChatMsg from "./notAllowedChatMsg";
import { useChatDataContextValue } from "../../../context/chatDataContext";


export default function OpenChatConnectionManager(){
    const { chatId } = useChatDataContextValue()

    const chatData = getChatData(chatId);
    const notAllowedChatIds = getUserNotAllowedIds();

    return(
        <div className="grid grid-cols-[300px_1fr] w-screen h-screen overflow-auto">
            <OpenChatSideBar />

            {notAllowedChatIds.includes(chatId) ? (
                <NotAllowedChatMsg />
            ) : 
            
            chatData ? (
                <ManageAddUserToChat />
            ) : 
            
            <ManageNewChatConection />}
        </div>
    )
}