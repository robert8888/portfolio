export function getUrlAnchor(): string{
    return window.location.hash;
}

export function setUrlAnchor(tag: string): void{
    history.pushState(null, "", location.origin + location.pathname + '#' + tag.replace("#", ""))
}