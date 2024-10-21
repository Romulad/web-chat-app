

export function setUserToken(token: string){
    localStorage.setItem('token', token)
}

export function getUserToken(){
    return localStorage.getItem('token')
}