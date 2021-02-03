import { createApp, App } from 'vue';

import storePlugin from "./store"

import Gallery from "./components/Gallery.vue";

customElements.define('vue-component', class extends HTMLElement{
  private app: App | undefined;

  createComponent(){
     this.app = createApp({
         components: {Gallery},
     })
     this.app.use(storePlugin)
     this.app.mount(this, true)
  }

  connectedCallback(){
    this.createComponent();
  }

  disconnectedCallback(){
      if(!this.app) return;
      this.app.unmount(this)
  }
})
