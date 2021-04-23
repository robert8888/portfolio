
<template slot="item">
  <main class="navigation navigation--main">
    <button class="navigation__btn"
            @click="toggle"
            :aria-expanded="expanded"
            aria-label="Menu expand">
    </button>
    <nav id="mainNavContainer" :class="['navigation__container', {'navigation__container--collapsed': !expanded}]">
      <ul class="navigation__list" ref="container">
        <slot/>
      </ul>
    </nav>
  </main>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import {useStore, MUTATIONS} from "@/store";
import scrollDisableMixin from "./../mixins/scrollDisable";

export default defineComponent({
  mixins: [scrollDisableMixin],

  setup(){
    const store = useStore();
    return {
      expanded: computed(() => store.state.menu.expanded),
      toggle: () => store.commit(MUTATIONS.TOGGLE_MENU_MAIN),
    }
  },

  mounted() {
    const localLinks = (this.$refs.container as HTMLElement).querySelectorAll('a[href*="#"]');
    for(const link of localLinks){
      link.addEventListener('click', () =>{
        this.toggle();
      })
    }
  },

  watch: {
    expanded: function(){
      this.expanded && window.matchMedia('(max-width: 1280px)').matches
          ? this.scrollDisable() : this.scrollEnable();
    }
  }

})


</script>
