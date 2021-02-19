<template>
  <li class="slider__item" v-size="updateSize" :style="{margin: '5px ' + itemMargin + 'px' }">
    <slot/>
  </li>
</template>

<script lang="ts">
import {defineComponent, inject} from 'vue';

export default defineComponent({
  props:{

  },

  data(){
    return {
      size: new DOMRect(),
      itemMargin: 0,
    }
  },

  setup(){
    const containerSize = inject('containerSize') as DOMRect;
    const numberOfItems = inject('numberOfItems') as number;
    const emitMargin = inject('onMargin') as (m: number, min: boolean) => void;

    return {containerSize, numberOfItems, emitMargin};
  },


  methods:{
    updateSize(rect: DOMRect){ this.size = rect; },


    updateMargin(){
      const minMargin = 20;
      const width = this.containerSize.width;
      const whole = Math.min(Math.floor((width - minMargin) / (this.size.width + minMargin)), this.numberOfItems) || 1;
      const marginSum = width - (whole * this.size.width);
      if(isNaN(marginSum))
        return;
      let margin = marginSum / whole / 2;
      let isMin = false;
      if(margin < minMargin){
        margin = minMargin;
        isMin = true;
      }
      this.emitMargin(margin, isMin);
      this.itemMargin = margin;
    },
  },

  computed: {
    widths: function (): string{
      if(!this.containerSize.width || !this.size.width) return "";
      return this.containerSize.width.toString() + "-" + this.size.width.toString();
    }
  },

  watch: {
    //@ts-ignore
    widths(){ this.updateMargin()}
  }
})

</script>
<style>
.slider__item{
  width: 100%;
  display: inline-flex;
  justify-content: center;
  will-change: margin;
}
</style>