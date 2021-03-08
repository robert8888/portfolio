export function getUrlAnchor(){
    return window.location.hash;
}

export function setUrlAnchor(tag: string){
    history.pushState(null, "", location.origin + location.pathname + '#' + tag.replace("#", ""))
}