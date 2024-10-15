

export default function Overlay(
    {showOverlay, onOverlayClick} : {showOverlay: boolean, onOverlayClick?: (()=>void)}
){
    const commonClasses = "fixed w-full h-full top-0 left-0 bg-[rgba(0,0,0,0.5)] z-[999]";
    let className = "";

    if(showOverlay){
        className = commonClasses;
    }else{
        className = commonClasses + " hidden";
    }

    return(
        <div className={className} onClick={onOverlayClick}>
        </div>
    )
}