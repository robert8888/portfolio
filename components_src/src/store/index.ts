
import { InjectionKey, App} from 'vue'
import { createStore, useStore as baseUseStore, Store as BaseStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";
import {menu, card, projects} from "./modules";
import {MenuState} from "@/store/modules/menu";
import {CardState} from "@/store/modules/card";
import {ProjectsState} from "@/store/modules/projects";
export { GETTERS, MUTATIONS, ACTIONS } from "./modules"

export interface RootState {
  menu: MenuState;
  card: CardState;
  projects: ProjectsState;
}

export const key: InjectionKey<BaseStore<RootState>> = Symbol()

export const store = createStore<RootState>({
  modules:{ menu, card, projects },
  plugins: [createPersistedState({
    paths: [
        'projects.projects',
        'card'
    ]
  })]
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

