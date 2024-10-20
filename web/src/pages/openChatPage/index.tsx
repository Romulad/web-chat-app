

export default function OpenChatPage(){
    return(
        <div>
            {JSON.stringify(localStorage.getItem('openChat'))}
        </div>
    )
}