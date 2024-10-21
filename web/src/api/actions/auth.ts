import { defaultAppState } from "../../lib/constant";
import {  UserChatHistoryResp, UserDataResp, UserTokenResp } from "../../lib/definitions";
import { request } from "../request";
import { getAboutUserDataRoute, getCreateAccountRoute, getUserChatHistoriesRoute } from "../routes";


export const createUserAccount = async (
    email: string, firstName: string, password: string, lastName?: string,
): Promise<{reqState: string, respData: UserTokenResp | any}> => {

    const reqData = {
        email,
        first_name: firstName,
        last_name: lastName || "",
        password
    }

    try{
        const resp = await request.post(getCreateAccountRoute(), reqData);
        return {reqState: defaultAppState.success, respData: resp.data}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: error?.response?.data}
    }
}

export const fetchAboutUserData = async () : Promise<{reqState: string, respData: UserDataResp | any}> => {
    try{
        const resp = await request.get(getAboutUserDataRoute());
        return {reqState: defaultAppState.success, respData: resp.data}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: error?.response?.data}
    }
}

export const fetchUserChatHistories = async () : Promise<{reqState: string, respData: UserChatHistoryResp | any}> => {
    try{
        const resp = await request.get(getUserChatHistoriesRoute());
        return {reqState: defaultAppState.success, respData: resp.data}
    }catch(error:any){
        console.log(error?.response?.data || error?.request || error?.message)
        return {reqState: defaultAppState.error, respData: error?.response?.data}
    }
}