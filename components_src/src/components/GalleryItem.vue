<template>
  <li class="gallery__item">
    <img :src="src" alt="" :width="containerSize.w"/>
  </li>
</template>

<script lang="ts">
import {inject, computed, defineComponent} from 'vue';

interface Size{
  w: number;
  h: number;
}

export default defineComponent({
  setup(){
    const containerSize = inject('containerSize') as Size;
    return {containerSize:  containerSize};
  },
  props:{
    src: String,
  },
  data: function(){
    return {
    }
  },

  watch:{
    containerSize(){
      //@ts-ignore
      //console.log(this.containerSize)
    }
  }
})

</script>
