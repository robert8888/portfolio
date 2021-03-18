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
import {defineComponent, computed} from "vue";
import Spinner from "./Spinner.vue";
import shallowArrayEqual from "@/utils/shallow-array-compare";
import getCaptchaToken from "@/utils/get-captcha-token";

export type ErrorList = Array<{
  message: string;
  field: string;
}>

interface ComponentData {
  message: string;
  isSuccessMessage: boolean;
  fieldsMap: Map<string, Element>;
  validationErrors: ErrorList;
  isSending: boolean;
}

type HTMLFormField = HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | HTMLButtonElement ;

type FormControlsCollection = HTMLFormControlsCollection & {
  [key: string]: HTMLFormField;
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
      message: "",
      isSuccessMessage: false,
      fieldsMap: new Map<string, HTMLFormField>(),
      validationErrors: [] as ErrorList,
      isSending: false,
    }
  },

  provide(){
    return {
      registerFieldId: (id: string) => {
        const form = this.$refs.form as HTMLFormElement;
        const elements = form.elements as FormControlsCollection;
        this.fieldsMap.set(id, elements[id])
        this.clientValidation(elements[id])
      },

      validationErrors: computed(() => this.validationErrors)
    }
  },

  methods: {
    async submit(e: Event) {
      e.preventDefault();

      this.isSending = true;
      this.clearValidation();

      const token = await getCaptchaToken();
      const csrfToken = window.csrfToken  as string;

      const data = [...this.fieldsMap].reduce((data, [id, element]) => ({
            ...data,
            [id]: (element as HTMLFormField).value
          }),
          {
          gRrecaptchaRresponse: token,
          csrfMiddlewareToken: csrfToken
        })

      const origin = location.origin
      const path = location.pathname

      const response = await fetch(`${origin}${path}api/contact-form`, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          "X-CSRFToken": csrfToken
        },
        referrerPolicy: 'origin',
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .catch(() => {
        this.message = this.errorMessage;
        this.isSuccessMessage = false;
      }).finally(() => {
        this.isSending = false;
      })

      response.success
          ? this.setSuccessMessage()
          : this.setValidationMessages(response.errors as ErrorList)
    },

    clientValidation(element: HTMLFormField){
      element.addEventListener('invalid', (event: Event) => {
          event.preventDefault();

          const id = (event.target as HTMLFormField).getAttribute("id");
          const name = (event.target as HTMLFormField).getAttribute("aria-label");

          if(!id || !name)
            return;

          const message = `${name} is required`
          this.setValidationMessages([...this.validationErrors, {field: id, message}]);
      });

      element.addEventListener('input', (event: Event) => {
          const element = event.target as HTMLFormField;
          if(!element.checkValidity())
              return
          const id = element.getAttribute("id");
          const validationErrors = this.validationErrors.filter(error => error.field !== id)
          if(!shallowArrayEqual(validationErrors, this.validationErrors))
            this.setValidationMessages(validationErrors)
      });
    },

    clearValidation(){
      this.message = ""
      this.fieldsMap.forEach((element) => {
        const label = element?.closest('label')
        label?.removeAttribute('data-validation-msg');
      })
    },

    setValidationMessages(errors: ErrorList){
      this.validationErrors = errors;
      this.isSuccessMessage = false;

      errors.length
        ? this.message = this.validationMessageFail //"Not all form fields have been filled in correctly"
        : this.message = ""

      errors.forEach(({message, field}) => {
        const formElement = this.fieldsMap.get(field);
        const label = formElement?.closest('label')
        label?.setAttribute('data-validation-msg', message);
      })
    },

    setSuccessMessage(){
      this.message = this.validationMessageSuccess;//"The message has reached me, I will contact back to you.";
      this.isSuccessMessage = true;
      this.fieldsMap.forEach(element => {
        (element as HTMLFormField).value = ""
      })
    },

  },
})
</script>