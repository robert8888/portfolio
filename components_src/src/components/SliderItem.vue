<template>
  <li class="slider__item"
      v-size="updateSize"
      :data-index="index"
      :style="{margin: '5px ' + itemMargin + 'px' }">
    <slot/>
  </li>
</template>

<script lang="ts">
import {defineComponent, inject} from 'vue';

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
    return {itemMargin, sizeChange}
  },

  methods:{
    updateSize(rect: DOMRect){
      this.size = rect;
    },
  },

  watch: {
    size(){
      this.sizeChange(this.size)
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