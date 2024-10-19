

type RemoteMsgDisplayProps = {
    msg: string;
    name?: string;
}

export default function RemoteMsgDisplay(
    {name, msg}: RemoteMsgDisplayProps
){
    return(
        <div className="me-auto max-w-96 flex items-start gap-2">
            {name &&
            <div className="border-2 px-4 py-2 rounded-full">
                {name.charAt(0).toUpperCase()}
            </div>}

            <div className="mt-5 bg-slate-100 rounded-tr-xl rounded-bl-xl rounded-br-xl p-4 pt-1">
                {name &&
                <span className="font-semibold">
                    {name}
                </span>}

                <p className="mt-3">
                    {msg}
                </p>
            </div>
        </div>
    )
}