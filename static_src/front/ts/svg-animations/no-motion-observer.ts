interface ReferencedValue {
    current: any;
}

export function getNoMotionObserver(): ReferencedValue{
    const value = {} as ReferencedValue;

    const matchMedia = window.matchMedia("(prefers-reduced-motion: reduce)");

    value.current = matchMedia && matchMedia.matches;

    matchMedia.addEventListener("change", () => {
        value.current = matchMedia && matchMedia.matches
    })

    return value;
}

