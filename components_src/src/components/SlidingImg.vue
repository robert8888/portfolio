<template>
  <div class="sliding-img">
    <img v-bind:src="src" alt=""/>
  </div>
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