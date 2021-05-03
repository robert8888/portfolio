
export interface MenuState {
    mainExpanded: boolean;
}

export const MUTATIONS = {
    TOGGLE_MENU_MAIN: "toggle",
}

export const ACTIONS = {

}

export const GETTERS = {

}

export default {
    state: (): MenuState => ({
        mainExpanded: false,
    }),
    mutations: {
        [MUTATIONS.TOGGLE_MENU_MAIN](state: MenuState): void {
            state.mainExpanded = !state.mainExpanded;
        },
    },

    actions: {

    },
    getters: {

    }
}
