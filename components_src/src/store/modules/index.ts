export {default as counter} from "@/store/modules/counter";

import {
    MUTATIONS as COUNTER_MUTATION,
    ACTIONS as COUNTER_ACTIONS,
    GETTERS as COUNTER_GETTERS,
} from "@/store/modules/counter";

export const MUTATIONS = {
    ...COUNTER_MUTATION
}

export const ACTIONS = {
    ...COUNTER_ACTIONS
}

export const GETTERS = {
    ...COUNTER_GETTERS
}