import {defineComponent} from "vue"

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
        scrollCancel(){
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