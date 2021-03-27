(function (){
    const delta = 10;
    let wasScrolled = false;
    let lastScrollPosition = 0;

    window.addEventListener('scroll', () => wasScrolled = true)

    const getScrollDirection = () => {
        const position = window.scrollY;
        const diff = lastScrollPosition - position;
        if(Math.abs(diff) > delta){
            lastScrollPosition = position;
            return diff < 0 ? "up" : "down"
        }
        return ""
    }

    const setDirection = () =>{
        if(!wasScrolled)
            return;
        const direction = getScrollDirection();
        if(!direction)
            return;
        document.body.setAttribute('data-scroll-direction', direction);
        wasScrolled = false;
    }

    setInterval(() => {
        setDirection();
    }, 250)
})()