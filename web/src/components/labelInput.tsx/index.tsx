import React from "react";

interface LabelInputProps extends React.InputHTMLAttributes<HTMLInputElement>{
    label: string;
    name: string;
    type?: string; 
    placeholder?: string;
}

export default function LabelInput(
    {
        label,
        name,
        type="text",
        placeholder="",
        ...attrs
    } : LabelInputProps
){
    return(
        <div className="mb-4">
            <label htmlFor={name}>
                {label}
            </label>

            <input 
            type={type} name={name} id={name}
            className="block w-full mt-3 border rounded-lg p-3 bg-slate-50" 
            placeholder={placeholder}
            {...attrs}/>    
        </div>
    )
}