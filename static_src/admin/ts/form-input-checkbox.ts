// wrapping element in additional div for styling
(function (){
    const inputs = document.querySelectorAll("input[type=checkbox]");
    for(let input of inputs){
        createWrapper(input as HTMLElement)
    }
    function createWrapper(input: HTMLElement){
        const wrapper = document.createElement('div');
        wrapper.className = 'input--checkbox input__wrapper';
        const layer = document.createElement('div');
        layer.className = 'input__overlay'
        input.classList.add('input')
        input.parentNode?.insertBefore(wrapper, input);
        wrapper.appendChild(input)
        wrapper.appendChild(layer)
    }
})()