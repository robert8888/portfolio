<template v-slot="gallery">
  <div class="gallery">
     <div class="gallery__container">
        <ul class="gallery__items">
          <slot/>
        </ul>
        <button>prev</button>
        <button>next</button>
        <button>close</button>
     </div>
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
