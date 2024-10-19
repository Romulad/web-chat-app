import { useEffect, useRef, useState } from "react";
import { parseSocketData } from "../lib/functions";
import { openChatRespDataScheme } from "../lib/definitions";


export default function useWebSocket(
    url: string, 
    onOpen?: ((ev: Event, ws?: WebSocket) => void),
    onMessage?: ((data: openChatRespDataScheme, ws?: WebSocket) => void)
){
    const [isInAction, setIsInAction] = useState(true);
    const [initializing, setInitializing] = useState(true);
    const ws = useRef<WebSocket>();
    
    useEffect(()=>{
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
            setIsInAction(false);
        })

        return () => { websocket.close() }
    }, [])

    return {
        ws: ws.current,
        isInAction, 
        setIsInAction,
        initializing
    };
}