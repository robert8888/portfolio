export default {
    data(){
        return {
            lastScrollPosition: 0,
        }
    },
    methods:{
        scrollDisable(){
            document.body.style.overflow = "hidden";
            // @ts-ignore
            this.lastScrollPosition = window.pageYOffset;
        },
        scrollEnable(){
            document.body.style.overflow = "auto";
            // @ts-ignore
            window.scrollTo(0, this.lastScrollPosition)
        }
    }
}