
/**
 * Throttling enforces a maximum number of times a function
 * can be called over time.
 *
 * @param func a function
 * @param wait time
 */
export function throttle(this: any, func: Function, wait: number) {
    let timeout:  number | null = null;
    let callbackArgs: any[];
    const context = this;

    const later = () => {
        func.apply(context, callbackArgs);
        timeout = null;
    };

    return function(...args: any[]) {
        if (!timeout) {
            callbackArgs = args;
            timeout = setTimeout(later, wait);
        }
    };
}