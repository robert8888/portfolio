import {App} from "vue";
import { nanoid } from 'nanoid'

const observers = new Map<string, ResizeObserver>();

const resizeObserveDirective = {
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

        update(el.getBoundingClientRect());

        observers.set(id, observer);
    },
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