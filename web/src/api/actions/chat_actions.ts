import { defaultAppState } from "../../lib/constant";
import { createOpenChatResp, UserListResp } from "../../lib/definitions";
import { request } from "../request";
import { getCreateOpenChatRoute, getDeleteOpenChatRoute, getFindUserRoute } from "../routes";


export const createNewOpenChat = async (
    chatId: string, initiatorId: string, initiatorName: string, chatName: string
): Promise<{reqState: string, respData: createOpenChatResp}> => {

    const reqData = {
        chat_id: chatId,
        initiator_id: initiatorId,
        initiator_name: initiatorName,
        chat_name: chatName
    }

    try{
        const resp = await request.post(getCreateOpenChatRoute(), reqData);
        return {reqState: defaultAppState.success, respData: resp.data}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: error?.response?.data}
    }
}

export const deleteOpenChat = async (
    chatId: string
): Promise<{reqState: string, respData: boolean | null}> => {
    try{
        await request.delete(getDeleteOpenChatRoute(chatId));
        return {reqState: defaultAppState.success, respData: true}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: null}
    }
}

export const searchUsers = async (query: string) : Promise<{reqState: string, respData: UserListResp | any}> => {
    try{
        const resp = await request.get(getFindUserRoute(), {params: {q: query}});
        return {reqState: defaultAppState.success, respData: resp.data}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: error?.response?.data}
    }
}