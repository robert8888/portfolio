<template>
  <teleport to="body" v-if="isOpen">
    <div class="modal__container" @click="containerClick">
      <div class="modal">
        <slot/>
      </div>
    </div>
  </teleport>
</template>
<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  emits: ["close"],

  props: {
    open:{
      type: Boolean,
      default: false,
    },
  },

  data(){
    return {
      isOpen: this.open
    }
  },

  methods:{
    containerClick(event: Event): void{
        if((event.target as HTMLElement).closest(".modal"))
          return;
        this.isOpen = false;
        this.$emit("close")
    }
  },

  watch:{
    open(){
      this.isOpen = this.open;
    }
  }
})
</script>
<style lang="scss" scoped>
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

  max-width: 600px;
  min-width: 280px;
  width: 400px;

  max-height: 300px;
  min-height: 180px;


}
</style>