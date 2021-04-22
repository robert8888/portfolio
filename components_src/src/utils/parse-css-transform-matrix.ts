export default function parseMatrix(value: string){
    const regex = /^matrix\((?<scaleX>[\d.-]*),\s*(?<skewY>[\d.-]*),\s(?<skewX>[\d.-]*),\s(?<scaleY>[\d.-]*),\s(?<translateX>[\d.-]*),\s(?<translateY>[\d.-]*)/
    return value.match(regex)?.groups
}