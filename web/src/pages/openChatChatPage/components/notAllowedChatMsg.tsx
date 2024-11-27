import { getUserOpenChatInfo } from "../../../lib/functions";


export default function NotAllowedChatMsg(){
    const userData = getUserOpenChatInfo();

    return(
        <div className="h-screen flex justify-center items-center text-center">
            <div className="text-center">
                <p>
                    Your user id: <b>{userData?.userId || ""}</b>
                </p> <br />
                <p>
                    You can have access to this chat for now. <br />
                    Ask an admin to explicitly add you to the chat with your user id
                </p>
            </div>
        </div>
    )
}