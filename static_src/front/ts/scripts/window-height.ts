(function (){
    const updateStyleInnerHeightProperty = () => {
        document.documentElement.style.setProperty('--vh', (window.innerHeight / 100).toString() + 'px');
    }
    window.addEventListener('resize', updateStyleInnerHeightProperty);
    updateStyleInnerHeightProperty();
})()