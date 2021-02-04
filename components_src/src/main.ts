import { createApp, App } from 'vue';

import storePlugin from "./store"

import * as components from "./components";

customElements.define('vue-component', class extends HTMLElement{
  private app: App | undefined;

  createComponent(){
    this.app = createApp({ components })
    this.app.use(storePlugin)
    this.setAttribute("data-server-rendered", "true");
    this.app.mount(this, true);
  }

  connectedCallback(){
    this.createComponent();
  }

  disconnectedCallback(){
    if(!this.app) return;
    this.app.unmount(this)
  }
})
