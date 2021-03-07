export function getUrlParams(): Map<string, string[]>{
    const params = new Map<string, string[]>()
    const search = window.location.search.replace("?", "");
    if(!search) return params;
    search.split("&").forEach(param => {
        const [name, value] = param.split("=");
        let values = params.get(name) || [];
        values = [...values, ...value.split(",")];
        params.set(name, values);
    })
    return params
}

export default function getUrlParam(name: string): string[]{
    const params = getUrlParams();
    return  params.get(name) || [] as string[];
}

