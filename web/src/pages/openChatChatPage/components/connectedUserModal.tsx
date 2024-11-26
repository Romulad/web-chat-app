import { CenteredModalContainer } from "../../../components";
import { connectedOpenChatUserRespData } from "../../../lib/definitions";



export default function ConnectedUserModal(
    {
        toggleUserListModal,
        showUserListModal,
        chatUsers,
        connectedIds
    } : {
        toggleUserListModal: () => void;
        showUserListModal: boolean;
        chatUsers: Array<connectedOpenChatUserRespData>,
        connectedIds: string[]
    }
){
    return(
        <CenteredModalContainer 
        closeModal={toggleUserListModal} 
        showModal={showUserListModal}>
            <div className="bg-white rounded-lg ">
                <h2 className="p-4">
                    {chatUsers.length > 1 ? "Users" : "User"}
                </h2>

                <ul className="max-h-[60vh] overflow-auto divide-y-2">
                    {chatUsers &&
                    chatUsers.map((chatuser)=>(
                        <li className="p-4" key={chatuser.user_id}>
                            <div className="flex items-center gap-3 ">
                                <div className="border px-4 py-2 rounded-full">
                                    {chatuser.name.charAt(0).toUpperCase()}
                                </div>
                                <div className="flex flex-col gap-2">
                                    <p className="">
                                        {chatuser.name}
                                    </p>
                                    <span className="flex gap-2 items-center">
                                        {chatuser.is_owner &&
                                        <span className="bg-black rounded-full px-2 text-white text-xs">
                                            Admin
                                        </span>}
                                        {connectedIds?.includes(chatuser.user_id) &&
                                        <span className="bg-green-300 rounded-full px-2 text-black text-xs">
                                            Connected
                                        </span>}
                                    </span>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </CenteredModalContainer>
    )
}