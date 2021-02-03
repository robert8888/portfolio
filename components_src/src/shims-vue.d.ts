/* eslint-disable */
declare module '*.vue' {
  import { Component } from 'vue'
  const component: Component
  export default component
}

import { Store } from 'vuex'
import State from "./store/state";

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $store: Store<State>;
  }
}

