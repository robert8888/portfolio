import {defineComponent} from "vue"
import windowScrollHeight from "@/utils/window-scroll-height";

interface MixinState{
    lastScrollPosition: number;
}

export default defineComponent({
    data(): MixinState{
        return {
            lastScrollPosition: 0,
        }
    },
    methods:{
        scrollCancel(event: Event){
            window.scrollTo(0, this.lastScrollPosition)
        },
        scrollDisable(){
            this.lastScrollPosition = window.pageYOffset;
            window.addEventListener('scroll', this.scrollCancel)
        },
        scrollEnable(){
            window.removeEventListener('scroll', this.scrollCancel)
        }
    }
})