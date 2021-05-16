
<template slot="item">
  <main class="navigation navigation--main">
    <button class="navigation__btn"
            @click="toggle"
            :aria-expanded="expanded"
            aria-label="Menu expand">
    </button>
    <nav v-if="!isMobile"  :class="['navigation__container']">
      <ul class="navigation__list" ref="container">
        <slot/>
      </ul>
    </nav>
    <teleport v-if="isMobile && expanded" to="body">
      <div class="navigation--main">
        <nav id="mainNavContainer" :class="['navigation__container', 'navigation__container--mobile']">
          <ul class="navigation__list" ref="container">
            <slot/>
          </ul>
        </nav>
      </div>
    </teleport>
  </main>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import {useStore, MUTATIONS} from "@/store";
import scrollDisableMixin from "./../mixins/scrollDisable";

interface ComponentState{
  matchMobile: MediaQueryList | null;
  isMobile: boolean;
}

export default defineComponent({

  data(): ComponentState{
    return {
      matchMobile: null,
      isMobile: false,
    }
  },

  setup(){
    const store = useStore();
    return {
      expanded: computed(() => store.state.menu.mainExpanded),
      toggle: () => store.commit(MUTATIONS.TOGGLE_MENU_MAIN),
      hide: () => store.commit(MUTATIONS.HIDE_MENU_MAIN),
      show: () => store.commit(MUTATIONS.SHOW_MENU_MAIN),
    }
  },

  mounted(){
    this.matchMobile = window.matchMedia('(max-width: 1280px)')
    this.matchMobile.addEventListener('change', this.mobileMatchChange)
    this.isMobile = this.matchMobile.matches;
  },

  unmounted() {
    this.matchMobile?.removeEventListener('change', this.mobileMatchChange)
  },


  methods:{
    mobileMatchChange(event: {matches: boolean}){
      this.isMobile = event.matches;
    }
  },

})


</script>
