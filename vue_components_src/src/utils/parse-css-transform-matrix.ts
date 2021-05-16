interface Matrix {
    scaleX: string;
    skewY: string;
    skewX: string;
    scaleY: string;
    translateX: string;
    translateY: string;
}

export default function parseMatrix(value: string): Matrix{
    const regex = /^matrix\((?<scaleX>[\d.-]*),\s*(?<skewY>[\d.-]*),\s(?<skewX>[\d.-]*),\s(?<scaleY>[\d.-]*),\s(?<translateX>[\d.-]*),\s(?<translateY>[\d.-]*)/
    const match = value.match(regex);
    return match?.groups as Matrix | Record<string, string> as Matrix
}