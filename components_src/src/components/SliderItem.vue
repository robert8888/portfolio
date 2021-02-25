<template>
  <li class="slider__item"
      v-size="updateSize"
      :style="{margin: '5px ' + itemMargin + 'px' }">
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
    }
  },

  setup(){
    const itemMargin = inject('itemMargin') as number;
    return {itemMargin}
  },

  methods:{
    updateSize(rect: DOMRect){
      this.size = rect;
    },
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