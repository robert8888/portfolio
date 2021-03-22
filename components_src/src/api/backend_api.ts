import {API_CONFIGURATION} from "./api_configuration";
import getCaptchaToken from "@/utils/get-captcha-token";

const csrfToken = (window as any).csrfToken  as string;

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
    return response.json()
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

export const getProjects = async(data: Record<string, any>): Promise<Record<string, any>> => {
    const apiPath = API_CONFIGURATION.GET_PROJECTS_URL

    let langPath = location.pathname.split("/")[1]
    langPath = langPath.length === 2 ? langPath + '/' : '';

    const path = `/${langPath}${apiPath}`;

    return request(path, data)
}