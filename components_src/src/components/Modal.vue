<template>
  <teleport to="body" v-if="isOpen">
      <div class="modal__container" v-if="isOpen" @click="containerClick">
        <div :class="['modal', $props.class,  {'modal--with-close-btn':!backdropClose }]">
          <button class="modal__btn-close" v-if="!backdropClose" @click="close"></button>
          <slot/>
        </div>
      </div>
  </teleport>
</template>
<script lang="ts">
import {defineComponent, ref} from "vue";

export default defineComponent({
  emits: ["close"],

  props: {
    open:{
      type: Boolean,
      default: false,
    },
    class:{
      type: String
    },
    backdropClose: {
      type: Boolean,
      default: true
    }
  },

  setup() {
    return {
      container: ref(null),
    };
  },

  data(){
    return {
      isOpen: this.open
    }
  },


  methods:{
    close(){
      this.isOpen = false;
      this.$emit("close")
    },
    containerClick(event: Event): void{
        if(!this.backdropClose)
          return;
        if((event.target as HTMLElement).closest(".modal") || !(event.target as HTMLElement).closest("html"))
          return;
        this.close();
    }
  },

  watch:{
    open(){
      this.isOpen = this.open;
    }
  }
})
</script>
<style lang="scss">
.modal{
  &__container{
    --backdrop-color: #0009;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--backdrop-color);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

</style>