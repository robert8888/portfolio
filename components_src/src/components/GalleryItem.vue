<template>
  <li class="gallery__item">
    <img :src="src" alt="" :width="containerSize.w"  loading="lazy" />
  </li>
</template>

<script lang="ts">
import {inject,  defineComponent} from 'vue';

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
    thumbSrc: {
      type: String,
      required: true,
    },
    fullSrc: {
      type: String,
    }
  },

  computed:{
    src(): string{
      return this.containerSize.w > 300
          ? this.fullSrc || this.thumbSrc
          : this.thumbSrc;
    }
  },

})

</script>
