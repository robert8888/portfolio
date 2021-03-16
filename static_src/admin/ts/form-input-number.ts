
(function() {
    const update = (input: HTMLInputElement, sign: string,  event: Event) => {
        event.preventDefault();
        const precision = (input.getAttribute("step") || "").split(".")[1]?.length;
        const step = +(input.getAttribute("step") || "1");
        const max = +(input.getAttribute("max") || "Infinity");
        input.value = Math.min(
            +input.value + (sign === "plus" ? + step : - step)
            , max
        ).toFixed(precision);
        input.focus();
    }

    const inputs = document.querySelectorAll('input[type=number]')
    inputs.forEach(input  => {
        const parent = input.parentNode;
        if(!parent) return;
        parent.removeChild(input);

        const wrapper = document.createElement("div");
        const increaseButton = document.createElement("button");
        const decreaseButton = document.createElement("button");

        wrapper.className = "input-number__wrapper";
        input.className = "input-number";
        increaseButton.className = "input-number__btn input-number__btn--increase";
        decreaseButton.className = "input-number__btn input-number__btn--decrease";

        increaseButton.addEventListener('click', update.bind(null, <HTMLInputElement>input, "plus"))
        decreaseButton.addEventListener('click', update.bind(null, <HTMLInputElement>input, "minus"))

        wrapper.appendChild(input);
        wrapper.appendChild(increaseButton);
        wrapper.appendChild(decreaseButton);
        parent.appendChild(wrapper);
    })
})();