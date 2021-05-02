import {App} from "vue";
import { nanoid } from 'nanoid'

const observers = new Map<string, ResizeObserver>();

const resizeObserveDirective = {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    mounted(el: HTMLElement, binding: any) {
        const id = nanoid();
        binding.instance._resizeObserverId = id;

        const update = (rect: DOMRect) => {
            if(typeof binding.value !== "function")
                return;
            binding.value(rect)
        }

        const observer = new ResizeObserver((entries: ResizeObserverEntry[]) => {
            update(entries[0].contentRect)
        })
        observer.observe(el);

        observers.set(id, observer);
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    beforeUnmount(el: HTMLElement, binding: any) {
        if(binding.instance._resizeObserverId && observers.has(binding.instance._resizeObserverId)){
            const observer = observers.get(binding.instance._resizeObserverId);
            observer?.disconnect();
            observers.delete(binding.instance._resizeObserverId)
        }
    }
}

export default {
    install(app: App) {
        app.directive('size', resizeObserveDirective);
    }
}