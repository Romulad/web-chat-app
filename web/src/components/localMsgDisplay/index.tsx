

type LocalMsgDisplayProps = {
    msg: string;
    extraMsg?: string[];
    name?: string;
    showIcon?: boolean
}

export default function LocalMsgDisplay(
    {name, msg, showIcon, extraMsg} : LocalMsgDisplayProps
){
    return(
        <div className="ms-auto max-w-96 flex items-start gap-2">
            <div>
                <div className="mt-5 bg-violet-600 rounded-tl-xl rounded-bl-xl rounded-br-xl p-4 pt-1 text-white">
                    {name &&
                    <span className="font-bold">
                        {name}
                    </span>}

                    <p className="mt-3">
                        {msg}
                    </p>
                </div>

                {extraMsg && extraMsg.length &&
                extraMsg.map((msg, index)=>(
                    <div key={index}
                    className="mt-1 bg-violet-600 rounded-tl-xl rounded-bl-xl rounded-br-xl p-4 pt-1 text-white">
                        {msg}
                    </div>
                ))}
            </div>
            
            {name && showIcon &&
            <div className="border-2 px-4 py-2 rounded-full">
                {name?.charAt(0).toUpperCase()}
            </div>}
        </div>
    )
}