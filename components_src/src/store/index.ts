
import { InjectionKey, App} from 'vue'
import { createStore, useStore as baseUseStore, Store as BaseStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";
import {counter, menu} from "./modules";
import {CounterState} from "@/store/modules/counter";
import {MenuState} from "@/store/modules/menu";
export { GETTERS, MUTATIONS, ACTIONS } from "./modules"

export interface RootState {
  counter: CounterState;
  menu: MenuState;
}

export const key: InjectionKey<BaseStore<RootState>> = Symbol()

export const store = createStore<RootState>({
  modules:{ counter, menu },
  plugins: [createPersistedState()]
})

export function useStore(){
  return baseUseStore<RootState>(key)
}

export default {
  store,
  install(app: App) {
    app.use(store, key);
  }
}

