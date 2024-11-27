

type RemoteMsgDisplayProps = {
    msg: string;
    extraMsg?: string[];
    name?: string;
    showIcon?: boolean
}

export default function RemoteMsgDisplay(
    {name, msg, showIcon, extraMsg}: RemoteMsgDisplayProps
){
    return(
        <div className="me-auto max-w-96 flex items-start gap-2">
            {name && showIcon &&
            <div className="border-2 px-4 py-2 rounded-full">
                {name.charAt(0).toUpperCase()}
            </div>}

            <div>
                <div className="mt-5 bg-slate-100 rounded-tr-xl rounded-bl-xl rounded-br-xl p-4 pt-1">
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
                    className="mt-1 bg-slate-100 rounded-tr-xl rounded-bl-xl rounded-br-xl p-4 pt-1">
                        {msg}
                    </div>
                ))}
            </div>
        </div>
    )
}