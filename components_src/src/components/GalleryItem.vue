<template>
  <li class="gallery__item">
    <img v-bind:src="src" alt=""/>
  </li>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  props:{
    src: String,
  },
  data: function(){
    return {
      src: this.src
    }
  }
})

</script>
