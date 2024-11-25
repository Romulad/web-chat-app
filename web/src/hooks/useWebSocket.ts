import { useEffect, useRef, useState } from "react";
import { parseSocketData } from "../lib/functions";
import { openChatRespDataScheme } from "../lib/definitions";
import { toast } from "react-toastify";


export default function useWebSocket(
    url: string, 
    onOpen?: ((ev: Event, ws?: WebSocket) => void),
    onMessage?: ((data: openChatRespDataScheme, ws?: WebSocket) => void)
){
    const [isInAction, setIsInAction] = useState(false);
    const [initializing, setInitializing] = useState(false);
    const ws = useRef<WebSocket>();
    const retryCount = useRef(0);
    
    useEffect(()=>{
       function establishConnection(){
        setInitializing(true);
        setIsInAction(true);
        const websocket = new WebSocket(url);

        websocket.addEventListener('open', (ev)=>{
            ws.current = websocket;
            setInitializing(false);
            setIsInAction(false);
            onOpen && onOpen(ev, websocket);
        })

        websocket.addEventListener('message', (ev)=>{
            const respData = parseSocketData(ev.data);
            setIsInAction(false);
            onMessage && onMessage(respData, websocket);
        })

        websocket.addEventListener('error', (_)=>{
            setInitializing(false);
            setIsInAction(false);
            toast.error('An error has occured');
            setTimeout(() => {
                if(websocket.readyState !== WebSocket.OPEN && 
                    websocket.readyState !== WebSocket.CLOSED
                ){
                    websocket.close();
                }
            }, 5000);
        })

        websocket.addEventListener('close', (_)=>{
            setInitializing(false);
            setIsInAction(false);
            if(retryCount.current <= 10){
                setTimeout(() => {
                    toast.error('Attempting connection again...');
                    establishConnection();
                }, (retryCount.current + 1) * 5000); 
            }
            retryCount.current++;
        })
       }

       establishConnection()

        return () => { ws.current?.close() }
    }, [url])

    return {
        ws: ws.current,
        isInAction, 
        setIsInAction,
        initializing
    };
}