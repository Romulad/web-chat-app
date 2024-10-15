import React from "react";

interface LabelInputProps extends React.InputHTMLAttributes<HTMLInputElement>{
    label: string;
    name: string;
    type?: string; 
    placeholder?: string;
    inputError?: string;
}

export default function LabelInput(
    {
        label,
        name,
        type="text",
        placeholder="",
        inputError,
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

            {inputError && 
            <p className="text-red-500 text-sm mt-2">{inputError}</p>}  
        </div>
    )
}