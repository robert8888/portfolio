<template>
  <div class="spinner component">
    <div class="spinner__ring"/>
    <span class="spinner__label">{{label}}</span>
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "spinner",
  props:{
    label:{
      type: String,
    }
  },
})

</script>
<style lang="scss">
.spinner{
  --spinner-color: #0f8bc6;
  --spinner-bg-color: #b7b7bf;
  --spinner-thicknes: 4px;
  --spinner-width: 32px;
  --spinner-height: 32px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  &__ring{
    border-style: solid;
    border-width: var(--spinner-thicknes);
    border-color: var(--spinner-color) var(--spinner-bg-color) var(--spinner-bg-color);
    width: var(--spinner-width);
    height: var(--spinner-height);
    animation-name: spinner-rotate;
    border-radius: 50%;
    animation-duration: .8s;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }
  &__label{
    margin-left: 15px;
    &:first-letter{
      text-transform: uppercase;
    }
  }
  @keyframes spinner-rotate {
    from{ transform: rotate(0deg)}
    to { transform: rotate(360deg)}
  }
}
</style>