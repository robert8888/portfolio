<template>
  <div :class="['card-project', {'card-project--collapsed': !isExpanded}]">
    <header>
      <h3>{{title}}</h3>
      <button class="card-project__btn card-project__btn--max" @click="toggle"/>
    </header>
    <div class="card-project__content">
      <slot/>
      <div :class="['card-project__additional', {'card-project__additional--collapsed': !isExpanded}]">
        <slot name="additional"/>
      </div>
     <footer>
       <a class="card-project__link card-project__link--more" :href="href" tabindex="0">vist page</a>
     </footer>
    </div>
  </div>
</template>
<script>
import {computed, defineComponent} from "vue";
import {MUTATIONS, useStore} from "@/store";

export default defineComponent({
  name: 'card-project',

  props: {
    title: String,
    href: String,
  },

  setup(){
    const store = useStore();
    return {
      isExpanded: computed(() => store.state.card.isExpanded),
      toggle: () => store.commit(MUTATIONS.TOGGLE_EXPAND),
    }
  },

})
</script>