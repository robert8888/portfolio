<template>
  <label :for="$props.for" :class="['form__label', $props.class]">
    <slot/>
    <span class="form__label-text">{{label}}</span>
    <p class="form__validation-message">{{validationMessage}}</p>
  </label>
</template>
<script lang="ts">
import {defineComponent, inject, computed} from "vue";
import {ErrorList} from "./ContactForm.vue";

export default defineComponent({
  props:{
    pattern: {
      type: String,
    },
    label: {
      type: String,
      required: true,
    },
    for: {
      type: String,
      required: true,
    },
    class: {
      type: String,
    }
  },

  data(){
    return {
      validationMessage: ""
    }
  },

  setup(props){
    const registerId = inject("registerFieldId") as (id: string) => void;
    const validationErrors = inject('validationErrors') as ErrorList
    return { registerId ,validationErrors};
  },

  mounted() {
    this.registerId(this.for);
  },

  watch:{
    validationErrors(){
      if(this.validationErrors)
        this.validationMessage =
            this.validationErrors.find(error => error.field === this.for)?.message || ""
    }
  }

})
</script>