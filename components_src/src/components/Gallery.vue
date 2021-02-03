<template>
  <div class="gallery">
    <h4>tekst</h4>
    <h1>value {{value}}</h1>
    <slot/>
    <button v-on:click="increment">more</button>
    <button v-on:click="decrement">less</button>
  </div>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import {useStore} from "@/store";

export default defineComponent({
  setup(){
    const store = useStore();
    return {
      value: computed(() => store.state.counter.value),
      increment: () => store.commit('increment', 1),
      decrement: () => store.commit('decrement', 1)
    }
  }
})


</script>
