import {getUrlParams} from "@/utils/get-url-param";

function isString(value: string | string[]): value is string{
    return typeof value === "string"
}

export function getSearchString(params: Map<string, string[]>): string{
    const search = [...params.entries()]
        .filter(([, values]) => values.length)
        .reduce((search, [name, values], index ) => {
            search += index ? "&" : "?"
            search += `${name}=${values.join(',')}`
            return search;
        }, "")
    return search
}

export default function setUrlParam(name: string, value: string | string[]): void{
    const values = isString(value) ? [value] : value;
    const params = getUrlParams();
    params.set(name, values);
    const search = getSearchString(params)
    window.history.pushState(null, '',  search ? search : location.pathname)
}