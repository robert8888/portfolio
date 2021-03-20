<template>
  <div class="projects">
    <div class="projects__container">
      <slot/>
    </div>
    <div class="projects__loading-container" ref="loading" :style="[loading ? {display: 'block'} : {display: 'none'}]">
      <div class="card-project--demo"/>
      <div class="card-project--demo"/>
      <div class="card-project--demo"/>
      <div class="card-project--demo"/>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import Spinner from "@/components/Spinner.vue";

export default defineComponent({
  components: {Spinner},

  data(){
    return {
      loading: false
    }
  }
})
</script>
