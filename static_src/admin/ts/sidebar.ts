(function(){
    window.addEventListener('load', () =>{
        const main = document.getElementById("main")
        if(!main) return;
        let collapsed = !main.classList.contains('shifted');

        const collapse = () =>{
            if(collapsed) return;
            main.classList.remove("shifted")
            collapsed = true;
        }

        const expand = () => {
            if(!collapsed) return;
            main.classList.add('shifted');
            collapsed = false;
        }

        const resizeObserver = new ResizeObserver((entries: ResizeObserverEntry[]) =>{
            entries[0].contentRect.width < 1024
                ? collapse()
                : expand();
        })

        resizeObserver.observe(document.body);
    })
})()
