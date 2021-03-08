export default function getAttributeObserveValue(target: HTMLElement, attributeName: string){
    const current = {
        value: target.getAttribute(attributeName)
    };

    const observer = new MutationObserver((mutationRecord) => {
        console.log(mutationRecord)
        mutationRecord.forEach((mutation) => {
            if(mutation.type !== "attributes" || mutation.attributeName !== attributeName)
                return;
            //@ts-ignore
            current.value = mutation.target[attributeName]
        })
    })

    observer.observe(target, {
        attributeFilter: [attributeName],
        subtree: false,
    })

    return current;
}