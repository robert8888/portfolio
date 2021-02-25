<template>
  <a :class="$props.class" @click="linkClick" :aria-role="$attrs.ariaRole">
    <slot/>
  </a>
  <modal :open="modalOpen" @close="onModalClose">
    <spinner v-if="isLoading"/>
    <div v-if="!isSuccess" class="error-message__container">
      <p class="error-message">{{errorMessage}}</p>
    </div>
    <div class="phone-number__container">
      <span v-if="number" class="phone-number">{{number}}</span>

    </div>



  </modal>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import Modal from "./Modal.vue";
import {load} from "recaptcha-v3";
import getCaptchaToken from "@/utils/getCaptchaToken";
import Spinner from "@/components/Spinner.vue";

export default defineComponent({
  components: {Spinner, Modal},

  props: {
    class: {
      type: String
    }
  },

  data(){
    return{
      modalOpen: false,
      number: "",
      isLoading: false,
      errorMessage: "Retrieve a number from the database failed",
      isSuccess: true,
    }
  },

  methods:{
    async getNumber(){
      this.isLoading = true;
      try{
        const captchaToken =  await getCaptchaToken();
        const csrfToken = (window as any).csrfToken  as string;

        const response = await fetch(origin + "/api/contact-phone", {
          method: 'POST',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrfToken
          },
          referrerPolicy: 'origin',
          body: JSON.stringify({
            captchaToken,
          })
        })

        const data = await response.json();
        this.number = data.number;

      } catch(error){
        this.isSuccess = false;
      } finally{
        this.isLoading = false
      }
    },

    linkClick(): void{
      this.modalOpen = true;
      if(!this.number)
        this.getNumber();
    },

    onModalClose(): void{
      this.modalOpen = false;
    }
  }

})
</script>