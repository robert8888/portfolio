<template>
  <div class="pdf-configurator__tpl">
    <div class="pdf-configurator__tpl-wrapper">
      <slot/>
      <h5>{{name}}</h5>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";
export default defineComponent({
  props: {
    name:{
      type: String,
      required: true,
    },
    templateId:{
      type: String,
      required: true,
    }
  },

})
</script>