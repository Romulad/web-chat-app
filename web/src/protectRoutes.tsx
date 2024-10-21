import { Navigate } from "react-router-dom";
import { getUserToken } from "./api/utils";
import React from "react";
import { createAccountPath } from "./lib/paths";


export default function ProtectedRoute({children} : {children: React.ReactNode}){
    if(getUserToken()){
        return children
    }else{
        return <Navigate to={createAccountPath}/>
    }
}