<template>
  <div class="slider">
    <div class="slider__container" ref="container">
      <div class="slider__slides"
           ref="wrapper"
           :style="wrapperStyle">
        <slot/>
      </div>
    </div>
    <div class="slider__controls">
      <button class="btn btn--prev" @click="prev"/>
      <button class="btn btn--next" @click="next"/>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import toRange from "@/utils/to-range";

export default defineComponent({
  props:{
    fixedSlideWidth:{
      type: Number,
      required: true,
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
    }
  },

  computed:{
    wrapperStyle(): Record<string, string>{
      return {
        'width': this.wrapperWidth + 'px',
        '--slide-width': this.slideWidth + 'px',
        'transform': `translate(${this.index * -this.slideWidth}px)`,
      }
    }
  },

  mounted(){
    this.count = (this.$refs.wrapper as HTMLElement).children?.length
    const resizeObserver = new ResizeObserver((entries: ResizeObserverEntry[]) => {
        const width = entries[0].contentRect.width;
        this.visible = toRange(~~(width / this.fixedSlideWidth), 1, this.count)
        this.slideWidth = width / this.visible;
        this.wrapperWidth = this.slideWidth * this.count;
        // console.log(width, this.visible, this.slideWidth, this.wrapperWidth)
    })
    resizeObserver.observe(this.$refs.container as HTMLElement)
    this.resizeObserverDisconnect = () => resizeObserver.disconnect()
  },

  unmounted() {
    this.resizeObserverDisconnect()
  },

  methods:{
    set(index: number){
      this.index = toRange(index, 0 , this.count - this.visible)
    },
    next(){this.set(this.index + 1)},
    prev(){this.set(this.index - 1)}
  }
})
</script>
<style lang="scss">
.slider{
  &__contaier{
    overflow: hidden;
  }
  &__slides{
    display: flex;
    & > * {
      width: var(--slide-width);
    }
  }
  &__controls{
    pointer-events: none;
    button{
      pointer-events: all;
    }
  }
}
</style>