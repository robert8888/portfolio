<template>
  <label :for="$props.for" :class="['form__label', $props.class]">
    <slot/>
    <span class="form__label-text" v-if="label">{{label}}</span>
    <p class="form__validation-message">{{validationMessage}}</p>
  </label>
</template>
<script lang="ts">
import {defineComponent, inject, watch, ref} from "vue";
import {ErrorList} from "./ContactForm.vue";

export default defineComponent({
  props:{
    pattern: {
      type: String,
    },
    label: {
      type: String,
      required: false,
    },
    for: {
      type: String,
      required: true,
    },
    class: {
      type: String,
    }
  },


  setup(props){
    const registerId = inject("registerFieldId") as (id: string) => void;

    const validationErrors = inject('validationErrors') as { list: ErrorList }

    const validationMessage = ref("")

    watch(validationErrors, () => {
      validationMessage.value = validationErrors.list.find(error => error.field === props.for)?.message || ""
    })

    return { registerId , validationMessage};
  },

  mounted() {
    this.registerId(this.for);
  },


})
</script>