export const BASE_ROUTE = location.href.includes('localhost') ? 
    "http://127.0.0.1:8000/" : "http://ec2-35-180-138-45.eu-west-3.compute.amazonaws.com/open-chat-api/";

export const getBaseRoute = (forSocket=false) => {
    if(forSocket){
        return location.href.includes('localhost') ? 
        "ws://127.0.0.1:8000/" : 
        "ws://ec2-35-180-138-45.eu-west-3.compute.amazonaws.com/open-chat-api/";
    }else{
        return location.href.includes('localhost') ? 
        "http://127.0.0.1:8000/" : 
        "http://ec2-35-180-138-45.eu-west-3.compute.amazonaws.com/open-chat-api/";
    }
}