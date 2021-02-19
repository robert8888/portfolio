
export interface MenuState {
    expanded: boolean;
}

export const MUTATIONS = {
    TOGGLE_MENU_MAIN: "toggle",
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
        [MUTATIONS.TOGGLE_MENU_MAIN](state: MenuState) {
            state.expanded = !state.expanded;
        },
    },

    actions: {

    },
    getters: {

    }
}
