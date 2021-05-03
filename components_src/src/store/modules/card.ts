
export interface CardState {
    isExpanded: boolean;
    galleryItemIndexes: {[key: string]: number};
}

export const MUTATIONS = {
    TOGGLE_EXPAND: "toggle_expand",
    SET_GALLERY_INDEX: "set_gallery_item_index",
}

export const ACTIONS = {

}

export const GETTERS = {
    GET_GALLERY_INDEX: "get_gallery_item_index",
}

export default {
    state: (): CardState => ({
        isExpanded: false,
        galleryItemIndexes: {} as {[key: string]: number}
    }),

    mutations: {
        [MUTATIONS.TOGGLE_EXPAND](state: CardState): void{
            state.isExpanded = !state.isExpanded
        },

        [MUTATIONS.SET_GALLERY_INDEX](state: CardState, payload: {id: string; index: number}): void{
            state.galleryItemIndexes[payload.id] = payload.index;
        }
    },


    actions: {

    },

    getters: {
       [GETTERS.GET_GALLERY_INDEX]: (state: CardState): (id: string) => number =>
           (id: string): number => {
           return state.galleryItemIndexes[id]
       }
    }
}
