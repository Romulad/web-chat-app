import axios from "axios";
import { BASE_ROUTE } from "./constant";


export const request = axios.create({
    baseURL: BASE_ROUTE
})