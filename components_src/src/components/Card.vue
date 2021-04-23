<template>
  <div :class="['card-project', {'card-project--extended': isExpanded, 'card-project--collapsed': !isExpanded}]">
    <header>
      <slot name="header">
        <h4 class="card-project__title"><a :href="href">{{title}}</a></h4>
        <button
            v-if="extensible"
            class="card-project__btn card-project__btn--expand"
            @click="toggle"
            v-on:tochstart="toggle"
            aria-label="Expand card"
        />
      </slot>
    </header>
    <main class="card-project__container">
      <div class="card-project__gallery">
        <slot name="gallery"/>
      </div>
      <div class="card-project__content" :aria-expanded="isExpanded">
        <div class="card-project__col">
          <slot/>
        </div>
        <div class="card-project__col">
          <div :class="['card-project__additional', {'card-project__additional--collapsed': !isExpanded}]">
            <slot name="additional"/>
          </div>
          <footer>
            <a class="card-project__link card-project__link--more" :href="href" tabindex="0">{{moreText}}</a>
          </footer>
        </div>
      </div>
    </main>
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
    moreText: String,
    extensible: {
      type: Boolean,
      default: false,
    },
    id: {
      type: String,
      request: true,
    },
    type: {
      type: String,
    },
    onClickLink: {
      type: Boolean,
      default: false,
    }
  },

  setup(){
    const store = useStore();
    return {
      isExpanded: computed(() => store.state.card.isExpanded),
      toggle: () => {
        store.commit(MUTATIONS.TOGGLE_EXPAND)
      },
    }
  },

  provide(){
    return {
      id: this.id,
    }
  },


  methods:{
    test(){
      console.log("clicked")
    }
  }
})
</script>