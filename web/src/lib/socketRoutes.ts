// import { BASE_ROUTE } from "../api/constant"


export const getOpenChatSocketRoute = ( ) => {
    return location.href.includes('localhost') ? "ws://127.0.0.1:8000/open-chat/ws" : "wss://web-chat-app-0r03.onrender.com/open-chat/ws";
}