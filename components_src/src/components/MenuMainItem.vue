<template>
    <li class="navigation__item" @click="onClick">
        <slot/>
    </li>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import {MUTATIONS, useStore} from "@/store";


export default defineComponent({
  setup(){
    const store = useStore();
    return {
      hide: () => store.commit(MUTATIONS.HIDE_MENU_MAIN),
    }
  },

  methods:{
    onClick(event: Event){
      console.log((event.target as HTMLElement), (event.target as HTMLElement).querySelectorAll('a'))
      if((event.target as HTMLElement).closest('[href*="#"]'))
        this.hide();
    }
  }
})


</script>
