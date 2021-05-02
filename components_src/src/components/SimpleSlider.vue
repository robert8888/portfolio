<template>
  <div class="simple-slider">
    <div class="simple-slider__controls">
      <button class="btn btn--prev"
              @click="change('prev')"
              :disabled="isMin"
              tabindex="0"/>
      <button class="btn btn--next"
              @click="change('next')"
              :disabled="isMax"
              tabindex="0"/>
    </div>

    <div class="simple-slider__container" ref="container">
      <div class="simple-slider__slides"
           @mousedown="dragStart"
           @touchstart.passive="dragStart"
           @dragstart="() => false"
           ref="wrapper"
           :style="wrapperStyle">
        <slot/>
      </div>
    </div>

  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import toRange from "@/utils/to-range";
import parseMatrix from "@/utils/parse-css-transform-matrix";

export default defineComponent({
  props:{
    fixedSlideWidth:{
      type: Number,
      required: true,
    },
    id:{
      type: String,
    },
    ratioToSweepNext:{
      type: Number,
      default: 1/5,
    }
  },
  data(){
    return {
      resizeObserverDisconnect: () => {/**/},
      wrapperWidth: 0,
      slideWidth: 0,
      count: 0,
      visible: 1,
      index: 0,
      position: 0,
      animated: false,
    }
  },

  mounted(){
    const wrapper = this.$refs.wrapper as HTMLElement
    this.count = wrapper.children?.length
    const resizeObserver = new ResizeObserver((entries: ResizeObserverEntry[]) => {
      const first = !this.slideWidth;
      const width = entries[0].contentRect.width;
      this.visible = toRange(~~(width / this.fixedSlideWidth), 1, this.count)
      this.slideWidth = width / this.visible;
      this.wrapperWidth = this.slideWidth * this.count;
      if(first && this.id)
        this.set(parseInt(window.localStorage.getItem(this.id) || "0") || 0)
      else
        this.normalize();
    })
    resizeObserver.observe(this.$refs.container as HTMLElement)
    this.resizeObserverDisconnect = () => resizeObserver.disconnect()

    for(let slide of wrapper.children){
      slide.addEventListener('focus', (event: Event) => {
        event.preventDefault();
        const parent = (event.target as HTMLElement)?.parentElement;
        const siblings = Array.from(parent?.children || [])
        const index = siblings.indexOf(event.target as HTMLElement);
        this.onSlideFocus(index)
      })
    }
  },

  unmounted() {
    this.resizeObserverDisconnect()
  },

  computed:{
    wrapperStyle(): Record<string, string>{
      return {
        'width': this.wrapperWidth + 'px',
        '--slide-width': this.slideWidth + 'px',
        'transition-property': this.animated ? 'transform' : 'none',
        'transform': `translate(${this.position}px)`,
      }
    },
    minPosition(): number{
      return -(this.wrapperWidth - this.slideWidth * this.visible);
    },
    maxPosition(): number{
      return 0;
    },
    isMin(): boolean{ return this.index === 0},
    isMax(): boolean{ return this.index === this.count - this.visible}
  },

  methods:{
    updatePosition({position, index}: { position?: number; index?: number } = {}){
      if(position){
        this.position = toRange(position, this.minPosition, this.maxPosition);
        return
      }
      this.position = this.evalPosition(index)
    },
    evalPosition(index?: number){
        return (index || this.index) * -this.slideWidth;
    },
    evalIndex(position?: number){
        const style = window.getComputedStyle((this.$refs.wrapper as HTMLElement))
        const matrix = parseMatrix(style.transform) 
        return matrix?.translateX || 0;
    },
    set(index: number){
      this.index = toRange(index, 0 , this.count - this.visible)
      this.updatePosition();
      console.log("index after", this.index)
      console.log(this.evalPosition(this.index))
    },
    change(direction: 'next' | 'prev'){
      const nextIndex = direction === 'next' ? this.index + 1 : this.index -1;
      this.animated = true;
      this.set(nextIndex)
    },
    normalize(shift = 0){
      this.animated = true;
      let index = Math.round(this.position / -this.slideWidth);
      if(shift && Math.abs(shift) > this.ratioToSweepNext * this.slideWidth){
        index += shift > 0 ? 1 : -1;  
      }
      this.set(index)
    },

    dragStart(event: TouchEvent | MouseEvent){
      if(event.cancelable)
        event.preventDefault();

      this.animated = false;
      const startX = (event as TouchEvent).touches?.[0].clientX || (event as MouseEvent).clientX;
      const startPosition = parseFloat(parseMatrix(window.getComputedStyle(this.$refs.wrapper as HTMLElement)['transform'])?.translateX || "0")
      this.updatePosition({position: startPosition})

      let diff = 0;
      const move = (event: TouchEvent | MouseEvent) => {
        const clientX = (event as TouchEvent).touches?.[0].clientX || (event as MouseEvent).clientX;
        diff = startX - clientX;
        this.updatePosition({position: startPosition -diff})
      }

      const normalize = this.normalize.bind(this);
      const up = () => {
        window.removeEventListener('touchmove', move, {passive: true} as EventListenerOptions)
        window.removeEventListener('mousemove', move, {passive: true} as EventListenerOptions)
        window.removeEventListener('touchend', up);
        window.removeEventListener('mouseup', up);
        normalize(diff)
      }

      window.addEventListener('touchmove', move, {passive: true} as EventListenerOptions)
      window.addEventListener('mousemove', move)
      window.addEventListener('mouseup', up);
      window.addEventListener('touchend', up)

      return false;
    },

    onSlideFocus(focusIndex: number){
      const wrapperParent =  (this.$refs.wrapper as HTMLElement).parentElement

      if(wrapperParent)// preventing default on focus scroll into view
        wrapperParent.scrollLeft = 0;

      if(focusIndex < this.index){
        this.set(focusIndex)
      } else if(focusIndex >= this.index + this.visible){
         this.set(focusIndex - this.visible + 1 )
      }
        
    }
  },

  watch:{
    index(index: number){
      if(this.id){
        window.localStorage.setItem(this.id, index.toString())
      }
    }
  }

})
</script>
