import { defaultAppState } from "../../lib/constant";
import { createOpenChatResp } from "../../lib/definitions";
import { request } from "../request";
import { getCreateOpenChatRoute } from "../routes";


export const createNewOpenChat = async (
    chatId: string, initiatorId: string, initiatorName: string
): Promise<{reqState: string, respData: createOpenChatResp}> => {

    const reqData = {
        chat_id: chatId,
        initiator_id: initiatorId,
        initiator_name: initiatorName
    }

    try{
        const resp = await request.post(getCreateOpenChatRoute(), reqData);
        return {reqState: defaultAppState.success, respData: resp.data}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: error?.response?.data}
    }
}