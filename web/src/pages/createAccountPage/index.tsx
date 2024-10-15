import React, { useState } from "react"
import { LabelInput } from "../../components";

export default function CreateAccount(){
    const [formData, setFormData] = useState({
        email: "",
        first_name: "",
        password: "",
        last_name: "",
    });

    function onCreateAccountBtnClick(ev: React.MouseEvent | React.FormEvent){
        ev.preventDefault();
    }

    return(
        <div className="max-w-[400px] mx-auto mt-10">
            <div>
                <h1 className="text-xl font-semibold text-center">Create account</h1>

                <form action="" method="post" className="mt-6"
                onSubmit={onCreateAccountBtnClick}>
                    <LabelInput 
                    label="Email:"
                    name="email"
                    placeholder="Email address"
                    type="email"
                    required
                    value={formData.email}
                    onChange={(ev)=>{
                        setFormData((data)=>({...data, email:ev.target.value}))
                    }}/>

                    <LabelInput 
                    label="First name:"
                    name="first_name"
                    placeholder="First name"
                    type="text"
                    required
                    value={formData.first_name}
                    onChange={(ev)=>{
                        setFormData((data)=>({...data, first_name:ev.target.value}))
                    }}/>

                    <LabelInput 
                    label="Last name:"
                    name="last_name"
                    placeholder="Last name"
                    value={formData.last_name}
                    onChange={(ev)=>{
                        setFormData((data)=>({...data, last_name:ev.target.value}))
                    }}/>

                    <LabelInput 
                    label="Create a password:"
                    name="password"
                    placeholder="New password"
                    type="password"
                    required
                    value={formData.password}
                    onChange={(ev)=>{
                        setFormData((data)=>({...data, password:ev.target.value}))
                    }}/>
                </form>

                <button 
                onClick={onCreateAccountBtnClick}
                className="rounded-full px-6 py-3 bg-blue-500 text-white ">
                    Create account
                </button>
            </div>
        </div>
    )
}