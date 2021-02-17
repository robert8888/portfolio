
export interface MenuState {
    expanded: boolean;
}

export const MUTATIONS = {
    TOGGLE: "toggle",
}

export const ACTIONS = {

}

export const GETTERS = {

}

export default {
    state: () => ({
        mainExpanded: false,
    }),
    mutations: {
        [MUTATIONS.TOGGLE](state: MenuState) {
            state.expanded = !state.expanded;
        },
    },

    actions: {

    },
    getters: {

    }
}
