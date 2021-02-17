export {default as counter} from "@/store/modules/counter";
export {default as menu} from "@/store/modules/menu";

import {
    MUTATIONS as COUNTER_MUTATION,
    ACTIONS as COUNTER_ACTIONS,
    GETTERS as COUNTER_GETTERS,
} from "@/store/modules/counter";

import {
    MUTATIONS as MENU_MUTATION,
    ACTIONS as MENU_ACTIONS,
    GETTERS as MENU_GETTERS,
} from "@/store/modules/menu";

export const MUTATIONS = {
    ...COUNTER_MUTATION,
    ...MENU_MUTATION,
}

export const ACTIONS = {
    ...COUNTER_ACTIONS,
    ...MENU_ACTIONS
}

export const GETTERS = {
    ...COUNTER_GETTERS,
    ...MENU_GETTERS
}