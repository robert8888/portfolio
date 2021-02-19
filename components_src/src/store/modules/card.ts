
export interface CardState {
    isExpanded: boolean;
}

export const MUTATIONS = {
    TOGGLE_EXPAND: "toggle_expand",
}

export const ACTIONS = {

}

export const GETTERS = {

}

export default {
    state: () => ({
        isExpanded: false,
    }),

    mutations: {
        [MUTATIONS.TOGGLE_EXPAND](state: CardState){
            state.isExpanded = !state.isExpanded
        },
    },

    actions: {

    },

    getters: {

    }
}
