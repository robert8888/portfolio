(function (){
    const updateStyleInnerSize= () => {
        document.documentElement.style.setProperty('--vh', (window.innerHeight / 100).toString() + 'px');
        document.documentElement.style.setProperty('--vw', (window.innerWidth / 100).toString() + 'px');
    }
    window.addEventListener('resize', updateStyleInnerSize);
    updateStyleInnerSize();
})()