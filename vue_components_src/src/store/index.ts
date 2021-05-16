
import { InjectionKey, App} from 'vue'
import { createStore, useStore as baseUseStore, Store as BaseStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";
import {menu, card, projects, cv} from "./modules";
import {MenuState} from "@/store/modules/menu";
import {CardState} from "@/store/modules/card";
import {ProjectsState} from "@/store/modules/projects";
import {CvState} from "@/store/modules/cv";
export { GETTERS, MUTATIONS, ACTIONS } from "./modules"

export interface RootState {
  menu: MenuState;
  card: CardState;
  projects: ProjectsState;
  cv: CvState;
}

export const key: InjectionKey<BaseStore<RootState>> = Symbol()

export const store = createStore<RootState>({
  modules:{ menu, card, projects, cv },
  plugins: [createPersistedState({
    paths: [
        'projects.projects',
        'card',
        'cv.colorProfile',
        'cv.templatedId'
    ]
  })]
})

export function useStore(): BaseStore<RootState>{
  return baseUseStore<RootState>(key)
}

export default {
  store,
  install(app: App): void {
    app.use(store, key);
  }
}

