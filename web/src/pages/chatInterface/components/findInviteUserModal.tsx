import { useState } from "react";
import { Button, CenteredModalContainer } from "../../../components";
import classes from "../../../lib/classes";
import { searchUsers } from "../../../api/actions/chat_actions";
import { defaultAppState } from "../../../lib/constant";
import { UserListResp } from "../../../lib/definitions";


interface FindInviteNewUserModalProps {
    showModal: boolean,
    closeModal: () => void
}

export default function FindInviteNewUserModal(
    {showModal, closeModal} : FindInviteNewUserModalProps
){
    const [value, setValue] = useState('');
    const [searching, setSearching] = useState(false);
    const [searchResult, setSearchResult] = useState<UserListResp>()

    function onSearchBtnClick(){
        if(!value){
           return 
        }

        setSearching(true);
        searchUsers(value)
        .then((resp)=>{
            setSearching(false);
            if(resp.reqState === defaultAppState.success){
                console.log(resp.respData);
                setSearchResult(resp.respData)
            }
        })
    }

    return(
        <CenteredModalContainer
        closeModal={closeModal}
        showModal={showModal}>
            <div className="bg-white p-4 rounded-lg">
                <div className="flex items-center gap-3"> 
                    <input type="search" 
                    name="" id="" placeholder="Search by name or email"
                    className="bg-slate-50 p-3 rounded-lg w-full border grow"
                    value={value}
                    onChange={(ev)=>{setValue(ev.target.value)}}/>

                    <Button 
                    className={classes.btn.outlined}
                    defaultText="Find"
                    isInAction={searching}
                    isInActionText="Searching..."
                    onClick={onSearchBtnClick}/>
                </div>
            </div>
        </CenteredModalContainer>
    )
}