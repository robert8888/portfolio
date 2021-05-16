<template>
  <form class="form" @submit="submit" ref="form" :aria-label="ariaLabel">
    <div class="form__fields">
    <slot/>
    </div>
    <div class="form__summary">
      <div class="form__summary__group">
        <spinner v-if="isSending" label="sending"/>
        <p class="form__message" :data-succes="isSuccessMessage">{{message}}</p>
        <button class="form__btn form__btn--send">{{submitButtonLabel}}</button>
      </div>
    </div>
  </form>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import Spinner from "./Spinner.vue";
import {sendForm} from "@/api/backend_api";
import useFormValidation from "@/hooks/useFormValidation";
import useFromDataMapper from "@/hooks/useFromDataMapper";

export type ErrorList = Array<{
  message: string;
  field: string;
}>

interface ComponentData {
  isSending: boolean;
  lastSendTry: null | number;
}


export default defineComponent({
  components: {Spinner},

  props:{
    ariaLabel: {
      type: String,
    },
    validationMessageFail: {
      type: String,
      default: ""
    },
    validationMessageSuccess:{
      type: String,
      default: ""
    },
    errorMessage:{
      type: String,
      default: ""
    },
    submitButtonLabel:{
      type: String,
      default: "Send message"
    }
  },

  data(): ComponentData{
    return {
      isSending: false,
      lastSendTry: null,
    }
  },

  setup(props){
    return {
      ...useFormValidation(
          props.validationMessageFail,
          props.validationMessageSuccess,
          props.errorMessage,
      ),
      ...useFromDataMapper(),
    }
  },

  mounted() {
    this.setFormRef(this.$refs.form as HTMLFormElement)
  },

  methods: {
    async submit(e: Event) {
      e.preventDefault();

      const timeFromLastTry = new Date().getTime() - (this.lastSendTry || 0 )
      this.lastSendTry = new Date().getTime();

      if(timeFromLastTry < 2000){
        return;
      }

      this.isSending = true;
      this.clearValidation();

      const data = this.getData(this.fieldsMap);

      try{
        const response = await sendForm(data);

        if(response.success){
          this.setSuccessMessage();
          (this.$refs.form as HTMLFormElement).reset();
        } else {
          this.setValidationMessages(response.errors as ErrorList);
        }
      } catch {
        this.message = this.errorMessage;
        this.isSuccessMessage = false;
      } finally {
        this.isSending = false;
      }
    },
  },
})
</script>