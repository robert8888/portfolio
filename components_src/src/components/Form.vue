<template>
  <form ref="form">
    <slot/>
  </form>
</template>
<script lang="ts">
import {defineComponent} from "vue"
export default defineComponent({
  emits: ['mounted'],
  mounted() {
    this.$emit('mounted', this.$refs.form)
  }
})
</script>