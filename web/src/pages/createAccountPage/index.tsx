import React, { useState } from "react"

import { Button, LabelInput } from "../../components";
import { createUserAccount } from "../../api/actions/auth";
import { defaultAppState } from "../../lib/constant";
import { setUserToken } from "../../api/utils";
import { useNavigate } from "react-router-dom";
import { chatInterfacePath } from "../../lib/paths";
import classes from "../../lib/classes";

export default function CreateAccount(){
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "",
        first_name: "",
        password: "",
        last_name: "",
    });
    const [error, setError] = useState("");
    const [emailError, setEmailError] = useState("");
    const [creatingAccount, setCreatingAccount] = useState(false);

    async function onCreateAccountBtnClick(ev: React.MouseEvent | React.FormEvent){
        ev.preventDefault();
        setError('');
        setEmailError('')

        if(!formData.email || !formData.email.includes("@")){
            setEmailError('Please enter an email')
            return
        }else if(!formData.first_name || formData.first_name.length < 3){
            setError('Enter a first name (mininum 3 characters)')
            return
        }else if(!formData.password || formData.password.length < 8){
            setError('Enter a password (mininum 8 characters)');
            return
        }

        setCreatingAccount(true);
        const {reqState, respData} = await createUserAccount(
            formData.email, formData.first_name, formData.password, formData.last_name
        )
        setCreatingAccount(false);

        if(reqState === defaultAppState.success){
            setUserToken(respData?.access_token);
            navigate(chatInterfacePath);
        }else{
            if(respData?.detail && typeof respData?.detail === "object"){
                for(const detail of respData?.detail){
                    if(detail?.loc?.includes('email')){
                        setEmailError(detail?.msg)
                    }else{
                        setError(detail?.msg)
                    }
                }
                
            }else if(respData?.detail && typeof respData?.detail === "string"){
                setEmailError(respData?.detail)
            }
        }
    }

    return(
        <div className="max-w-[400px] mx-auto mt-10">
            <div>
                <h1 className="text-xl font-semibold text-center">Create account</h1>

                <form action="" method="post" className="mt-6"
                onSubmit={onCreateAccountBtnClick}>
                   {error && 
                   <p className="mb-5 text-red-500 text-center">
                        {error}
                    </p>}

                    <LabelInput 
                    label="Email:"
                    name="email"
                    placeholder="Email address"
                    type="email"
                    required
                    inputError={emailError}
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
                
                <Button 
                className={classes.btn.blue}
                defaultText="Create account"
                isInAction={creatingAccount}
                isInActionText="Creating"
                onClick={onCreateAccountBtnClick}/>
            </div>
        </div>
    )
}