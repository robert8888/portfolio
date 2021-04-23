<template>
  <div class="simple-slider">
    <div class="simple-slider__container" ref="container">
      <div class="simple-slider__slides"
           @mousedown="dragStart"
           @touchstart="dragStart"
           @dragstart="() => false"
           ref="wrapper"
           :style="wrapperStyle">
        <slot/>
      </div>
    </div>
    <div class="simple-slider__controls">
      <button class="btn btn--prev"
              @click="change('prev')"
              :disabled="isMin"/>
      <button class="btn btn--next"
              @click="change('next')"
              :disabled="isMax"/>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, nextTick} from "vue";
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
    this.count = (this.$refs.wrapper as HTMLElement).children?.length
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
    set(index: number){
      this.index = toRange(index, 0 , this.count - this.visible)
      this.updatePosition();
    },
    change(direction: 'next' | 'prev'){
      const nextIndex = direction === 'next' ? this.index + 1 : this.index -1;
      this.animated = true;
      this.set(nextIndex)
    },
    normalize(){
      this.animated = true;
      this.index = Math.round(this.position / -this.slideWidth)
      this.updatePosition()
    },

    dragStart(event: TouchEvent | MouseEvent){
      event.preventDefault();

      this.animated = false;
      const startX = (event as TouchEvent).touches?.[0].clientX || (event as MouseEvent).clientX;
      const startPosition = parseFloat(parseMatrix(window.getComputedStyle(this.$refs.wrapper as HTMLElement)['transform'])?.translateX || "0")
      this.updatePosition({position: startPosition})

      const move = (event: TouchEvent | MouseEvent) => {
        const clientX = (event as TouchEvent).touches?.[0].clientX || (event as MouseEvent).clientX;
        const diff = startX - clientX;
        this.updatePosition({position: startPosition -diff})
      }

      const normalize = this.normalize.bind(this);
      const up = () => {
        window.removeEventListener('touchmove', move, {passive: false} as EventListenerOptions)
        window.removeEventListener('mousemove', move, {passive: false} as EventListenerOptions)
        window.removeEventListener('touchend', up);
        window.removeEventListener('mouseup', up);
        normalize()
      }

      window.addEventListener('touchmove', move, {passive: false} as EventListenerOptions)
      window.addEventListener('mousemove', move)
      window.addEventListener('mouseup', up);
      window.addEventListener('touchend', up)

      return false;
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
