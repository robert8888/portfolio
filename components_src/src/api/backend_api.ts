import {API_CONFIGURATION} from "./api_configuration";
import getCaptchaToken from "@/utils/get-captcha-token";

const csrfToken = (window as any).csrfToken  as string;

interface Result {
    success: boolean;
    errors: { message: string; field: string }[];
    data: Record<string, any>;
}


const getLanguageFromPath = () =>{
    const langPath = location.pathname.split("/")[1]
    return langPath.length === 2 ? langPath + '/' : '';
}

const buildPath = (apiPath: string) => `/${getLanguageFromPath()}${apiPath}`;


const request = async (path: string, data:  Record<string, any>, clean= false) => {
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

    if(response.ok)
        return clean ? response : await response.json() as Promise<Result>

    return {
        success: false,
        errors: [{field: "_server", message: ''}],
        data: {}
    }

}


export const getRequest = async (path: string): Promise<Response> =>{
    if(path.startsWith(location.origin))
        path = path.replace(location.origin, '')

    return fetch(path, {method: 'GET', headers: {"X-CSRFToken": csrfToken}})
}



export const sendForm = async (data:  Record<string, any>): Promise<Result> => {
    const path = API_CONFIGURATION.POST_CONTACT_FORM_URL
    const token = await getCaptchaToken();
    Object.assign(data, {
        gRrecaptchaRresponse: token,
        csrfMiddlewareToken: csrfToken
    })
    return request(location.pathname + path, data) as Promise<Result>
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
    return request(buildPath(apiPath), data) as Promise<Result>
}

export const getAutocomplete = async(data: {input: string}): Promise<Result> => {
    const apiPath = API_CONFIGURATION.GET_AUTOCOMPLETE
    return request(buildPath(apiPath), data) as Promise<Result>
}


export type GetCVPayload = {
    templateId: string;
    colorProfileId: string;
    recruiterEmail: string;
    recruiterCompany: string;
    captchaToken?: string;
}
export const getCv = async (data: GetCVPayload): Promise<Response> => {
    const apiPath = API_CONFIGURATION.GET_CV;
    data.captchaToken = await getCaptchaToken()
    return request(buildPath(apiPath), data, true) as Promise<Response>
}