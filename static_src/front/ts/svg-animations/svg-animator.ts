import animationsConfigs from './svg-animation-keyframes.json';
import {AnimationKeyframes} from "./svg-animation-keyframes-type";
import {getNoMotionObserverValue} from "./no-motion-observer";
import getAttributeObserveValue from "./attribute-observe-value";


(function (){
    window.addEventListener("load", () => {
        const animated = document.querySelectorAll("[data-svg-animation]") || [];
            [...animated].forEach(target => {
                animateSvg(target as HTMLElement);
            })
    })


    const noAnimationValue = getNoMotionObserverValue();
    const dataInitScroll = getAttributeObserveValue(document.body, 'data-init-anchor-scroll');

    const noAnimation = () => noAnimationValue.current || dataInitScroll.value === "true";


    function animateSvg(target: HTMLElement ){
        const animations = animationsConfigs as any as AnimationKeyframes;
        const animationName = (target.getAttribute("data-svg-animation") || "" )
        const noscroll = (target.getAttribute("data-svg-animation-noscroll") || "") === "true"

        if(noscroll && !noAnimation())
            setBodyScroll(true);

        if(!animationName)
            return;

        const animationConfig = animations[animationName];

        const runningAnimations = new Array<Promise<Event | boolean>>();
        for(const rule of animationConfig){
            let element: Element | null;

            if(rule.element.children !== undefined){
                element = target.children[rule.element.children]
            } else if(rule.element.selector){
                element = target.querySelector(rule.element.selector);
            } else {
                continue;
            }

            if(noAnimation()){
                element?.setAttribute(rule.attribute, [...rule.values].pop() || "");
                runningAnimations.push(Promise.resolve(true));
                continue;
            }

            const animate = document.createElementNS("http://www.w3.org/2000/svg","animate");
            animate.setAttribute('attributeName', rule.attribute);
            animate.setAttribute('dur', rule.duration);
            animate.setAttribute('fill', rule.fill);
            animate.setAttribute('values', rule.values.reduce((value, current) => value += current + "; ", ""));
            if(rule?.keyTimes)
                animate.setAttribute("keyTimes", rule.keyTimes)
            element?.appendChild(animate);
            runningAnimations.push(new Promise((res, rej) => {
                 animate.addEventListener("endEvent", (e) => {
                     res(e)
                 })
            }))
        }

        Promise.all(runningAnimations).then(() => {
            target.dispatchEvent(new CustomEvent(`svg-animation-end`, {
                bubbles: true,
            }));
        })
    }

    function setBodyScroll(disabled: boolean){
        window.scrollTo(0,0)
        disabled
            ? window.onscroll = (e: Event) => window.scrollTo(0,0)
            : window.onscroll = null;
    }


    (() => {
        const logoWrapper =  document.getElementById("logoWrapper");
        const logoContainer = document.getElementById("logoContainer");

        if(!logoWrapper || !logoContainer)
            return;

        logoWrapper.addEventListener("svg-animation-end", (e) => {
            logoContainer.setAttribute("data-init-anim-finished", "true");

            const initPosition = logoContainer.getBoundingClientRect();
            logoWrapper.classList.remove('logo__wrapper--init');

            if(noAnimation()){
                setBodyScroll(false);
                return;
            }

            //forcing style calculation
            window.getComputedStyle(logoWrapper);
            const targetPosition = logoContainer.getBoundingClientRect()
            const diff = {
                x: initPosition.x - targetPosition.x,
                y: initPosition.y - targetPosition.y
            }
            const animation = logoContainer.animate([{
                transform: `translate(${diff.x}px,${diff.y}px)`
            },{
                transform: `translate(0,0)`,
            }], {
                duration: 600,
                fill: "forwards",
                easing: "cubic-bezier(.43,.11,.49,1.35)"
            })

            animation.onfinish = () => {
                setBodyScroll(false);
            }
        })
    })()
})()