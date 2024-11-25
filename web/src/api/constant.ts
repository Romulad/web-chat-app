export const BASE_ROUTE = location.href.includes('localhost') ? "http://127.0.0.1:8000/" : "https://web-chat-app-0r03.onrender.com/";

export const getBaseRoute = (forSocket=false) => {
    if(forSocket){
        return location.href.includes('localhost') ? 
        "ws://127.0.0.1:8000/" : 
        "wss://web-chat-app-0r03.onrender.com/";
    }else{
        return location.href.includes('localhost') ? 
        "http://127.0.0.1:8000/" : 
        "https://web-chat-app-0r03.onrender.com/";
    }
}