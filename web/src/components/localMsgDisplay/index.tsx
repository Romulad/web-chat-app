

type LocalMsgDisplayProps = {
    msg: string;
    name?: string
}

export default function LocalMsgDisplay(
    {name, msg} : LocalMsgDisplayProps
){
    return(
        <div className="ms-auto max-w-96 flex items-start gap-2">
            <div className="mt-5 bg-violet-600 rounded-tl-xl rounded-bl-xl rounded-br-xl p-4 pt-1 text-white">
                {name &&
                <span className="font-semibold">
                    {name}
                </span>}

                <p className="mt-3">
                    {msg}
                </p>
            </div>
            
            {name && 
            <div className="border-2 px-4 py-2 rounded-full">
                {name?.charAt(0).toUpperCase()}
            </div>}
        </div>
    )
}