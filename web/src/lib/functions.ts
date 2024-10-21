import { openChatData, OpenChatMsg, openChatOneData, openChatRespDataScheme, openChatUser } from "./definitions";

const alpha = "abcdefghijklmnopqrstuvwxyz";

export function updateUseropenChatData(chatId: string, isOwner=true){
    const openChatData: openChatData = JSON.parse(
        localStorage.getItem('openChat') || "[]"
    );
    openChatData.push({isOwner, chatId});
    localStorage.setItem("openChat", JSON.stringify(openChatData));
    return chatId
}
export function getUseropenChatData() : openChatData {
    return JSON.parse(localStorage.getItem('openChat') || "[]")
}
export function getChatData(chatId: string) : openChatOneData | undefined {
    const openChatData: openChatData = JSON.parse(
        localStorage.getItem('openChat') || "[]"
    );
    const data = openChatData.find((data) => data.chatId === chatId);
    if (data){
        return data
    }
    return data;
}
export function deleteUserOpenChat(chatId: string) {
    const openChatData: openChatData = JSON.parse(
        localStorage.getItem('openChat') || "[]"
    );
    const updatedData = openChatData.filter((data) => data.chatId !== chatId);
    localStorage.setItem('openChat', JSON.stringify(updatedData));
}


export function updateUserNotAllowedChatIds(chatId: string){
    const notAllowedChatIds: Array<string> = JSON.parse(
        localStorage.getItem('notAllowed') || "[]"
    );
    notAllowedChatIds.push(chatId);
    localStorage.setItem("notAllowed", JSON.stringify(notAllowedChatIds));
    return chatId
}
export function getUserNotAllowedIds() : Array<string> {
    return JSON.parse(localStorage.getItem('notAllowed') || "[]")
}


export function setUserOpenChatInfo(data: openChatUser){
    localStorage.setItem('openChatUser', JSON.stringify(data));
    return data;
}
export function getUserOpenChatInfo(): openChatUser | null {
    const data = JSON.parse(localStorage.getItem('openChatUser') || '{}');
    return Object.keys(data).length ? data : null;
}


export function setLsOpenChatMsgs(chatId: string, msgs: OpenChatMsg[]){
    const chatMsgs = JSON.parse(
        localStorage.getItem('openChatMsgs') || "{}"
    );

    chatMsgs[chatId] = msgs;
    localStorage.setItem('openChatMsgs', JSON.stringify(chatMsgs));
}
export function getOpenChatMsgs(chatId: string):  OpenChatMsg[] | [] {
    const chatMsgs = JSON.parse(localStorage.getItem('openChatMsgs') || "{}");  
    const chatMsg = chatMsgs && chatMsgs[chatId]; 
    return chatMsg?.length ? chatMsg : [];
}


export const generateRandomCharac = (len=6) => {
    let chara = "";
    for (let i = 0; i < len; i++){
        chara += alpha.charAt(Math.floor(Math.random() * 23))
    }
    return chara;
}  

export function generateChatId(){
    const timestamp = new Date().getTime();
    return `chat-${timestamp}-${generateRandomCharac()}`;
}

export function generateUserId(name: string){
    const timestamp = new Date().getTime();
    return `${name.replaceAll(" ", "")}-${timestamp}-${generateRandomCharac()}`;
}

export function validateNameInput(name: string){
    if(!name){
        return 'Please enter a valid name'
    }

    if(name.length < 3){
        return 'Minimum 3 characters'   
    }

    return true;

}

export function parseSocketData(data: string | any) : openChatRespDataScheme{
    return JSON.parse(data)
}