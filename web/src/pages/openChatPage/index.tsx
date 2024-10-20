import { Link } from "react-router-dom";
import { getUseropenChatData } from "../../lib/functions"
import { getOpenChatPath } from "../../lib/paths";


export default function OpenChatPage(){
    const chatData = getUseropenChatData();

    return(
        <div className="max-w-[500px] sm:mx-auto mx-3 mt-10 bg-slate-50 rounded-lg p-4">
            <ul className="divide-y-2">
               {chatData?.map((data)=>(
                    <li key={data.chatId}>
                        <Link to={getOpenChatPath(data.chatId)}
                        className="w-full block p-3 rounded-lg hover:bg-slate-100">
                            {data.chatId.slice(0, 30) + "..."}
                        </Link>
                    </li>
               ))}
            </ul>
        </div>
    )
}