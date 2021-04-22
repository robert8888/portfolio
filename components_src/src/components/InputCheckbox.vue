<template>
  <div class="checkbox">
    <div class="checkbox__input-wrapper">
      <input :class="['checkbox__input', className]"
             :id="id"
             :name="name"
             type="checkbox"
             :data-label="ariaLabel"
             :placeholder="placeholder"
             :autocomplete="autocomplete"
             :required="required">
        <div class="checkbox__box"/>
    </div>
    <p class="checkbox__text"><slot/></p>
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";
export default defineComponent({
  props: {
    className: String,
    id: String,
    name: String,
    placeholder: String,
    autocomplete: String,
    required: Boolean,
    ariaLabel: String,
  }
})
</script>