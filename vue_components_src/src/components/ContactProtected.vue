<template>
  <a :class="$props.class" @click="linkClick" :aria-role="$attrs.ariaRole">
    <slot/>
  </a>
  <modal :open="modalOpen" @close="onModalClose" class="contact-protected__modal" ref="modal">
    <div class="contact-protected__container">
      <transition name="fade-in" mode="out-in">
        <span v-if="data && !confirmMessage" :class="'contact-protected__' + type">{{data}}</span>
        <span v-else>{{confirmMessage}}</span>
      </transition>
      <spinner v-if="isLoading" :label="loadingLabel"/>
      <div v-if="!isSuccess && !isLoading" class="contact-protected__error-message__container">
        <p class="contact-protected__error-message">{{errorMessage}}</p>
      </div>
    </div>
    <div class="contact-protected__controls" ref="controls" @click="controlsClick">
      <slot name="controls"/>
    </div>
  </modal>
</template>
<script lang="ts">
import {defineComponent, nextTick} from "vue";
import Modal from "./Modal.vue";
import Spinner from "@/components/Spinner.vue";
import {getNumber, getEmail} from "@/api/backend_api";

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
    },
    errorMessage:{
      type: String,
      default: "Ops. What a shame :("
    },
    type:{
      type: String,
      required: true
    }
  },

  data(){
    return{
      modalOpen: false,
      data: "",
      isLoading: false,
      isSuccess: true,
      confirmMessage: "",
    }
  },

  methods:{
    async getNumber(){
      try{
        this.isLoading = true;
        const response = await getNumber()
        if(response.success)
          this.data = this.formatPhoneNumber(response.data.number);
        else
          this.isSuccess = false;
      } catch(error){
        this.isSuccess = false;
      } finally{
        this.isLoading = false;
      }
    },

    async getEmail(){
      try{
        this.isLoading = true;
        const response = await getEmail();
        if(response.success)
          this.data = response.data.email;
        else
          this.isSuccess = false;
      } catch(error) {
        this.isSuccess = false;
        console.log('error')
      } finally {
        this.isLoading = false;
      }
    },

    linkClick(): void{
      this.modalOpen = true;
      if(this.data)
        return;

      this.isSuccess = true;

      if(this.type === 'number'){
        this.getNumber();
      } else if(this.type === 'email') {
        this.getEmail();
      }
    },

    onModalClose(): void{
      this.modalOpen = false;
    },

    formatPhoneNumber(number: string): string{
      const cleanNumber = this.formatStripFormatting(number.toString());
      const match = cleanNumber.toString().match(new RegExp("(.{3})".repeat(4) + "?"))
      return match ? match.slice(1).join(" ") : "Ops. :("
    },

    formatStripFormatting(number: string): string{
      return number.replace(/\s/g, "");
    },

    controlsClick(event: Event): void{
      event.preventDefault();
      const target = event.target as HTMLElement;
      const actionName = target.getAttribute("data-action") as "copy" | "call" | 'write';
      const actionConfirm = target.getAttribute("data-action-confirm") as string
      if(!actionName || !this[actionName] || typeof this[actionName] !== "function")
        return;
      this[actionName](actionConfirm);
    },

    call(){
      const link = document.createElement("a");
      link.href = "tel:" + this.formatStripFormatting(this.data);
      link.click();
      setTimeout(() =>{
        this.modalOpen = false
      }, 1)
    },

    copy(msg: string){
      const textarea = document.createElement("textarea");
      textarea.innerText = this.formatStripFormatting(this.data)
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
      this.confirmMessage = msg;
      setTimeout(() => {
        this.confirmMessage = "";
        this.modalOpen = false
      }, 3000)
    },

    write(){
      const link = document.createElement("a");
      link.href = this.data.startsWith('mailto') ? this.data : "mailto:" + this.data;
      link.click();
      setTimeout(() =>{
        this.modalOpen = false
      }, 1)
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