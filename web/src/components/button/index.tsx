import React from "react";
import classes from "../../lib/classes";


interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>{
    isInAction: boolean;
    isInActionText: string;
    className: string;
    defaultText: string;
}

export default function Button(
    {
        isInAction,
        isInActionText,
        defaultText, 
        className,
        ...props
    } : ButtonProps
){
    return(
        <button className={isInAction ? classes.btn.disabled : className}
        disabled={isInAction}
        {...props}>
            {isInAction ? isInActionText : defaultText}
        </button>
    )
}