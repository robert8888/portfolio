<template>
  <div class="overlay">
    <div class="l-row">
      <button class="overlay__btn overlay__btn--open" @click="expand">{{buttonOpenText}}</button>
    </div>
    <div :class="['overlay__content', {
    'overlay__content--collapsed': isCollapsed}]"
    :aria-hidden="isCollapsed"
    >
      <button
          @click="collapse"
          class="overlay__btn overlay__btn--close"
          aria-label="Close">
      </button>
      <slot/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent} from 'vue';
import scrollDisableMixin from "./../mixins/scrollDisable";

export default defineComponent({
  mixins: [scrollDisableMixin],

  props: {
    buttonOpenText: String,
  },

  data(){
    return {
      isCollapsed: true,

    }
  },

  methods: {
    expand(){
      this.isCollapsed = false;
      this.scrollDisable()
    },
    collapse(){
      this.isCollapsed = true;
      this.scrollEnable();
    }
  }

})


</script>

<style lang="scss">
.overlay__content {
  position: fixed;
  top:0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 10000;
  overflow-y: auto;
  &--collapsed{
    display: none;
  }
}
</style>