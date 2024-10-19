import { CenteredModalContainer } from "../../../components";
import { connectedOpenChatUserRespData } from "../../../lib/definitions";



export default function ConnectedUserModal(
    {
        toggleUserListModal,
        showUserListModal,
        chatUsers,
    } : {
        toggleUserListModal: () => void;
        showUserListModal: boolean;
        chatUsers: Array<connectedOpenChatUserRespData>,
    }
){
    return(
        <CenteredModalContainer 
        closeModal={toggleUserListModal} 
        showModal={showUserListModal}>
            <div className="bg-white rounded-lg ">
                <h2 className="p-4">
                    {chatUsers.length > 1 ? "Connected users" : "Connected user"}
                </h2>

                <ul className="max-h-[60vh] overflow-auto divide-y-2">
                    {chatUsers &&
                    chatUsers.map((chatuser)=>(
                        <li className="p-4" key={chatuser.user_id}>
                            <div className="flex items-center gap-3 ">
                                <div className="border px-4 py-2 rounded-full">
                                    {chatuser.name.charAt(0).toUpperCase()}
                                </div>
                                <div>
                                    <p className="flex gap-3 items-center">
                                        <span>
                                            {chatuser.name}
                                        </span>
                                        {chatuser.is_owner &&
                                        <span className="bg-green-300 rounded-full px-2 text-white text-xs">
                                            Admin
                                        </span>}
                                    </p>
                                    <span className="text-sm text-gray-600">
                                        {chatuser.user_id}
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