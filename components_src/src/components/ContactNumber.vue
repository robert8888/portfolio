<template>
  <a :class="$props.class" @click="linkClick" :aria-role="$attrs.ariaRole">
    <slot/>
  </a>
  <modal :open="modalOpen" @close="onModalClose" class="contact-number__modal" ref="modal">
    <div class="contact-number__container">
      <transition name="fade-in" mode="out-in">
        <span v-if="number && !confirmMessage" class="contact-number__number">{{number}}</span>
        <span v-else>{{confirmMessage}}</span>
      </transition>
      <spinner v-if="isLoading" :label="loadingLabel"/>
      <div v-if="!isSuccess" class="contact-number__error-message__container">
        <p class="contact-number__error-message">{{errorMessage}}</p>
      </div>
    </div>
    <div class="contact-number__controls" ref="controls" @click="controlsClick">
      <slot name="controls"/>
    </div>
  </modal>
</template>
<script lang="ts">
import {defineComponent, nextTick} from "vue";
import Modal from "./Modal.vue";
import getCaptchaToken from "@/utils/get-captcha-token";
import Spinner from "@/components/Spinner.vue";

declare global {
  interface Window {
    csrfToken: string;
  }
}

export default defineComponent({
  components: {Spinner, Modal},

  props: {
    class: {
      type: String
    },
    loadingLabel:{
      type: String,
    }
  },

  data(){
    return{
      modalOpen: false,
      number: "",
      isLoading: false,
      errorMessage: "Ops. What a shame :(",
      isSuccess: true,
      confirmMessage: "",
    }
  },

  methods:{
    async getNumber(){
      this.isLoading = true;

      try{
        const captchaToken =  await getCaptchaToken();
        const csrfToken = window.csrfToken  as string;

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

        this.number = this.formatPhoneNumber(data.number);

      } catch(error){
        this.isSuccess = false;
      } finally{
        this.isLoading = false;
      }
    },

    linkClick(): void{
      this.modalOpen = true;
      if(!this.number)
        this.getNumber();
    },

    onModalClose(): void{
      this.modalOpen = false;
    },

    formatPhoneNumber(number: string): string{
      const match = number.toString().match(new RegExp("(.{3})".repeat(4) + "?"))
      return match ? match.slice(1).join(" ") : "Ops. :("
    },

    formatStripFormatting(number: string): string{
      return number.replace(/\s/g, "");
    },

    controlsClick(event: Event): void{
      event.preventDefault();
      const target = event.target as HTMLElement;
      const actionName = target.getAttribute("data-action") as "copy" | "call";
      const actionConfirm = target.getAttribute("data-action-confirm") as string
      if(!actionName || !this[actionName] || typeof this[actionName] !== "function")
        return;
      this[actionName](actionConfirm);
    },

    call(){
      const link = document.createElement("a");
      link.href = "tel:" + this.formatStripFormatting(this.number);
      link.click();
      setTimeout(() =>{
        this.modalOpen = false
      }, 1)
    },

    copy(msg: string){
      const textarea = document.createElement("textarea");
      textarea.innerText = this.formatStripFormatting(this.number)
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
      this.confirmMessage = msg;
      setTimeout(() => {
        this.confirmMessage = "";
        this.modalOpen = false
      }, 3000)
    }
  },



  mounted() {
    this.$watch('isLoading', (isLoading: boolean) => {
      nextTick(() => {
          const controlsContainer = this.$refs.controls as HTMLElement;
          if(!controlsContainer)
            return;
          const buttons = controlsContainer.querySelectorAll("button");
          [...buttons].forEach(button =>
              isLoading
                  ? button.setAttribute('disabled', "disabled")
                  : button.removeAttribute('disabled')
          )
      })
    }, {immediate: true})
  },


})
</script>