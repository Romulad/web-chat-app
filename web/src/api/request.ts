import axios from "axios";
import { BASE_ROUTE } from "./constant";
import { getUserToken } from "./utils";


export const request = axios.create({
    baseURL: BASE_ROUTE,
    headers: {
        "Authorization": `Bearer ${getUserToken()}`
    }
})