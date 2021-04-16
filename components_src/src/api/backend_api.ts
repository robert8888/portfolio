import {API_CONFIGURATION} from "./api_configuration";
import getCaptchaToken from "@/utils/get-captcha-token";

const csrfToken = (window as any).csrfToken  as string;

interface Result {
    success: boolean;
    error: string[];
    data: Record<string, any>;
}


const getLanguageFromPath = () =>{
    let langPath = location.pathname.split("/")[1]
    return langPath.length === 2 ? langPath + '/' : '';
}


const request = async (path: string, data:  Record<string, any>) => {
    const origin = location.origin

    const response = await fetch(`${origin}` + path, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrfToken
        },
        referrerPolicy: 'origin',
        body: JSON.stringify(data)
    })
    return await response.json() as Promise<Result>
}


export const getRequest = async (path: string): Promise<Response> =>{
    if(path.startsWith(location.origin))
        path = path.replace(location.origin, '')

    return fetch(path, {method: 'GET', headers: {"X-CSRFToken": csrfToken}})
}



export const sendForm = async (data:  Record<string, any>): Promise<any> => {
    const path = API_CONFIGURATION.POST_CONTACT_FORM_URL
    const token = await getCaptchaToken();
    Object.assign(data, {
        gRrecaptchaRresponse: token,
        csrfMiddlewareToken: csrfToken
    })
    return request(location.pathname + path, data)
}

export const getNumber = async (): Promise<any> => {
    const path = API_CONFIGURATION.GET_NUMBER_URL
    const data = {
        captchaToken:  await getCaptchaToken()
    }
    return request(location.pathname + path, data)
}

export const getProjects = async(data: Record<string, any>): Promise<Result> => {
    const apiPath = API_CONFIGURATION.GET_PROJECTS_URL

    const langPath = getLanguageFromPath()

    const path = `/${langPath}${apiPath}`;

    return request(path, data)
}

export const getAutocomplete = async(data: {input: string}): Promise<Result> => {
    const apiPath = API_CONFIGURATION.GET_AUTOCOMPLETE

    const langPath = getLanguageFromPath()

    const path = `/${langPath}${apiPath}`;

    return request(path, data)
}


