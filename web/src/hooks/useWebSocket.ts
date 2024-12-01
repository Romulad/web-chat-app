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
    const connectionPool = useRef<WebSocket[]>([]);
    const retryCount = useRef(0);
    const currentTimeOut = useRef<number>();
    
    useEffect(()=>{
       function establishConnection(){
        if(ws.current) return;

        setInitializing(true);
        setIsInAction(true);
        
        const websocket = new WebSocket(url);
        // maintain connection list when more than one connections are initialized
        connectionPool.current = [...connectionPool.current, websocket];

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
                currentTimeOut.current = setTimeout(() => {
                    if(!ws.current){
                        toast.info('Attempting connection again...');
                        establishConnection();
                    }
                }, (retryCount.current + 1) * 5000); 
            }
            retryCount.current++;
        })
       }

       establishConnection()

        return () => { 
            connectionPool.current.forEach((connection)=>{
                connection.close()
            });
            clearTimeout(currentTimeOut.current);
        }
    }, [url])

    return {
        ws: ws.current,
        isInAction, 
        setIsInAction,
        initializing
    };
}