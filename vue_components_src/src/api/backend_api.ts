import {API_CONFIGURATION} from "./api_configuration";
import getCaptchaToken from "@/utils/get-captcha-token";
import {Project} from "@/store/modules/projects";

declare global{
    interface Window{
        csrfToken: string;
    }
}

const csrfToken = window.csrfToken as string;

interface Result<D>{
    success: boolean;
    errors: { message: string; field: string }[];
    data: D;
}


const getLanguageFromPath = () =>{
    const langPath = location.pathname.split("/")[1]
    return langPath.length === 2 ? langPath + '/' : '';
}

const buildPath = (apiPath: string) => `/${getLanguageFromPath()}${apiPath}`;


const request = async <D, I>(path: string, data: I, clean= false) => {
    const origin = location.origin

    const response = await fetch(`${origin}` + path, {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrfToken
        },
        referrerPolicy: 'origin',
        body: JSON.stringify(data)
    })

    if(response.ok)
        return clean ? response : await response.json() as Promise<Result<D>>

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



export const sendForm = async (data:  Record<string, string>): Promise<Result<Record<string, string>>> => {
    const path = API_CONFIGURATION.POST_CONTACT_FORM_URL
    const token = await getCaptchaToken();
    Object.assign(data, {
        gRrecaptchaRresponse: token,
        csrfMiddlewareToken: csrfToken
    })
    return request<Record<string, string>, Record<string, string>>(location.pathname + path, data) as Promise<Result<Record<string, string>>>
}

export const getNumber = async (): Promise<Result<{number: string}>> => {
    const path = API_CONFIGURATION.GET_NUMBER_URL
    const data = {
        captchaToken:  await getCaptchaToken()
    }
    console.log(data.captchaToken)
    // return request<{number: string}, {captchaToken: string}>(location.pathname + path, data) as Promise<Result<{number: string}>>
    console.log("The path ", `/${path}`)
    return request<{number: string}, {captchaToken: string}>(`/${path}`, data) as Promise<Result<{number: string}>>
}

export const getEmail = async (): Promise<Result<{email: string}>> => {
    const path = API_CONFIGURATION.GET_EMAIL_URL
    const data = {
        captchaToken: await getCaptchaToken()
    }
    return request<{email: string}, {captchaToken: string}>(location.pathname + path, data) as Promise<Result<{email:string}>>
}

export const getProjects = async(data: Record<string, string>): Promise<Result<Project[]>> => {
    const apiPath = API_CONFIGURATION.GET_PROJECTS_URL
    return request<Record<string, string>, Record<string, string>>(buildPath(apiPath), data) as Promise<Result<Project[]>>
}

export const getAutocomplete = async(data: {input: string}): Promise<Result<string[]>> => {
    const apiPath = API_CONFIGURATION.GET_AUTOCOMPLETE
    return request(buildPath(apiPath), data) as Promise<Result<string[]>>
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