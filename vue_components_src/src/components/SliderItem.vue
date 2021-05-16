<template>
  <li class="slider__item"
      ref="container"
      v-size="updateSize"
      :data-index="index"
      :aria-hidden="!isVisible ? true : null"
      :tabindex="!isVisible ? -1 : null"
      :style="{margin: '5px ' + itemMargin + 'px' }">
    <slot/>
  </li>
</template>

<script lang="ts">
import {defineComponent, inject } from 'vue';

export default defineComponent({
  props:{
    index: {
      type: Number,
      default: 0
    }
  },

  data(){
    return {
      size: new DOMRect(),
    }
  },

  setup(){
    const itemMargin = inject('itemMargin') as number;
    const sizeChange = inject('itemSizeChange') as (rect: DOMRect) => void;
    const visibleIndexes = inject("visibleItems") as number[];
 
    return {itemMargin, sizeChange, visibleIndexes}
  },

  mounted(){
    if(!this.isVisible)
        this.removeFromTabindex();
  },

  methods:{
    updateSize(rect: DOMRect){
      this.size = rect;
    },
    getFocusableChildes(): NodeListOf<HTMLElement>{
      return (this.$refs.container as HTMLElement)?.querySelectorAll('a, button, input') || []
    },
    removeFromTabindex(){
      for(const element of this.getFocusableChildes()){
          element.setAttribute('tabindex', "-1");
      }
    },
    restoreTabIndex(){
      for(const element of this.getFocusableChildes()){
        element.removeAttribute('tabindex');
      }
    }
  },

  computed:{
    isVisible(): boolean{
      return this.visibleIndexes.includes(this.index) || false;
    }
  },

  watch: {
    size(){
      this.sizeChange(this.size)
    },
    isVisible(visible: boolean){
      if(visible){
        this.restoreTabIndex();
      } else {
        this.removeFromTabindex();
      }
    }
  },

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