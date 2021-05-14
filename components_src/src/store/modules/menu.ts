
export interface MenuState {
    mainExpanded: boolean;
}

export const MUTATIONS = {
    TOGGLE_MENU_MAIN: "toggle main menu",
    HIDE_MENU_MAIN: "hide main menu",
    SHOW_MENU_MAIN: "show main menu"
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
        [MUTATIONS.SHOW_MENU_MAIN](state: MenuState): void {
            state.mainExpanded = true;
        },
        [MUTATIONS.HIDE_MENU_MAIN](state: MenuState): void {
            state.mainExpanded = false;
        },
    },

    actions: {

    },
    getters: {

    }
}
