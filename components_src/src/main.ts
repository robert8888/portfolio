import { createApp, App } from 'vue';

import storePlugin from "./store"
// @ts-ignore
import ResizeObserver from "@/directives/ResizeObserver";

import * as components from "./components";

interface Profiles {
  [key: string]: {
    pluginInstance: any;
    options: {[key: string]: string | number | boolean};
  }[];
}

const profiles = {} as Profiles

customElements.define('vue-component', class extends HTMLElement{
  private app: App | undefined;

  createComponent(){
    this.app = createApp({ components })
    this.app.use(storePlugin);
    this.app.use(ResizeObserver);
    this.applyProfile(this.app);
    this.setAttribute("data-server-rendered", "true");
    this.app.mount(this, true);
  }

  applyProfile(app: App){
    const profileName = this.getAttribute("profile") as string;
    const profile = profiles[profileName];
    if(!profile) return;
    profile.forEach(plugin => {
      app.use(plugin.pluginInstance, plugin.options)
    })
  }

  connectedCallback(){
    this.createComponent();
  }

  disconnectedCallback(){
    if(!this.app) return;
    this.app.unmount(this)
  }
})
