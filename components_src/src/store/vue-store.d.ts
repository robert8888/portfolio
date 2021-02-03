import {Store} from "vuex";
import {State} from "./index";

declare module 'vue/types/vue' {
    interface Vue {
        $store: Store<State>
    }
}