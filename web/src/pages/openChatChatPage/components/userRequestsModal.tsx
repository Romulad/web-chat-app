import React, { useEffect, useState } from "react";
import { Button, CenteredModalContainer } from "../../../components";
import classes from "../../../lib/classes";
import { openChatConnectionMsgType } from "../../../lib/constant";
import {  openChatReqDataScheme, openChatRespDataScheme } from "../../../lib/definitions";
import { getUserOpenChatInfo, parseSocketData } from "../../../lib/functions";
import { toast } from "react-toastify";


export function OneRequestDisplay(
    {
        userRequest, 
        userRequests,
        setUserRequests,
        ws
    } : 
   {
        userRequest: openChatRespDataScheme, 
        userRequests: openChatRespDataScheme[],
        setUserRequests: React.Dispatch<openChatRespDataScheme[]>
        ws: WebSocket | undefined
    }
){
    const [rejecting, setRejecting] = useState(false);
    const userData = getUserOpenChatInfo();

    function manageRequest(requestType: string){
        const data : openChatReqDataScheme = {
            chat_id: userRequest.chat_id,
            data: "",
            owner_id: userData?.userId || "",
            type: requestType,
            user_id: userRequest.user_id || "",
            user_name: userRequest.user_name || "",
        };
        ws?.send(JSON.stringify(data));
        const updatedData = userRequests.filter((request) => 
            request.chat_id !== userRequest.chat_id || request.user_id !== userRequest.user_id
        );
        setUserRequests(updatedData);
    }

    function onRejectBtnClick(){
        setRejecting(true);
        manageRequest(openChatConnectionMsgType.request_not_approved)
        setRejecting(false);
    }

    function onAcceptBtnClick(){
        manageRequest(openChatConnectionMsgType.request_approved)
    }

    return(
        <li className="p-4">
            <div className="mb-4">
                <p className="flex gap-3 items-center">
                    {userRequest.user_name} asked to join the chat
                </p>
                <span className="text-sm text-gray-600">
                    {userRequest.user_id}
                </span>
            </div>
            <div className="flex justify-end gap-2 items-center">
                <Button 
                className={classes.btn.red}
                defaultText="Reject"
                isInAction={rejecting}
                isInActionText="Rejecting"
                onClick={onRejectBtnClick}/>

                <button className={classes.btn.green}
                onClick={onAcceptBtnClick}>
                    Accept
                </button>
            </div>
        </li>
    )
}

export default function UserRequestsModal(
    {
        toggleUserRequestsModal,
        showUserRequestsModal,
        userRequests,
        setUserRequests,
        ws,
    } : {
        toggleUserRequestsModal: () => void;
        showUserRequestsModal: boolean;
        userRequests: Array<openChatRespDataScheme>;
        setUserRequests: React.Dispatch<openChatRespDataScheme[]>;
        ws: WebSocket | undefined
    }
){

    useEffect(()=>{
        ws?.addEventListener("message", (ev)=>{
            const data = parseSocketData(ev.data);
            if(data.type === openChatConnectionMsgType.notification){
                toast.info(data.msg);
            }
        })
    }, [])

    return(
        <CenteredModalContainer 
        closeModal={toggleUserRequestsModal} 
        showModal={showUserRequestsModal}>
            <div className="bg-white rounded-lg ">
                <h2 className="p-4">
                    {userRequests.length > 1 ? "Requests" : "Request"}
                </h2>

                <ul className="max-h-[60vh] overflow-auto divide-y-2">
                    {userRequests &&
                    userRequests.map((userRequest, index)=>(
                        <OneRequestDisplay 
                        setUserRequests={setUserRequests}
                        userRequest={userRequest}
                        userRequests={userRequests}
                        ws={ws}
                        key={index}/>
                    ))}
                </ul>
            </div>
        </CenteredModalContainer>
    )
}