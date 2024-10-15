import { openChatUser } from "./definitions";

export function updateUserOpenChatIds(chatId: string){
    const openChatIds: Array<string> = JSON.parse(
        localStorage.getItem('openChat') || "[]"
    );
    openChatIds.push(chatId);
    localStorage.setItem("openChat", JSON.stringify(openChatIds));
    return chatId
}
export function getUserOpenChatIds() : Array<string> {
    return JSON.parse(localStorage.getItem('openChat') || "[]")
}


export function setUserOpenChatInfo(data: openChatUser){
    localStorage.setItem('openChatUser', JSON.stringify(data));
    return data;
}
export function getUserOpenChatInfo(): openChatUser | null {
    const data = JSON.parse(localStorage.getItem('openChatUser') || '{}');
    return Object.keys(data).length ? data : null;
}

export function generateChatId(){
    const timestamp = new Date().getTime();
    return `chat-${timestamp}`;
}
export function generateUserId(name: string){
    const timestamp = new Date().getTime();
    return `${name.replaceAll(" ", "")}-${timestamp}`;
}
