export interface ColorProfile{
    [key: string]: string;
}

export interface CvState {
    colorProfile: {
        id: string;
        colors: ColorProfile;
    };
    templatedId: string;
}

export const MUTATIONS = {
    SET_CV_COLOR_PROFILE_ID: 'set_color_profile_id',
    SET_CV_COLOR_PROFILE: 'Set_color_profile',
    SET_CV_TEMPLATE_ID: 'Set_template_id',
}

export const ACTIONS = {

}

export const GETTERS = {
    GET_CV_TEMPLATE_ID: "get_template_id",
    GET_CV_COLOR_PROFILE_ID: "get_color_profile_id",
    GET_CV_COLOR_PROFILE_COLORS: "get_color_profile_colors"
}

export default {
    state: () => ({
        colorProfile: {
            id: '',
            colors: {}
        },
        templatedId: ''
    }),

    mutations: {
        [MUTATIONS.SET_CV_COLOR_PROFILE_ID](state: CvState, payload: {id: string}){
            state.colorProfile.id = payload.id;
        },

        [MUTATIONS.SET_CV_COLOR_PROFILE](state: CvState, payload: {id: string; colors: ColorProfile}){
            state.colorProfile.id = payload.id;
            state.colorProfile.colors = payload.colors;
        },

        [MUTATIONS.SET_CV_TEMPLATE_ID](state: CvState, payload: {id: string}){
            state.templatedId = payload.id;
        }
    },


    getters: {
        [GETTERS.GET_CV_TEMPLATE_ID]: (state: CvState) => {
           return state.templatedId
        },
        [GETTERS.GET_CV_COLOR_PROFILE_ID]: (state: CvState) => {
            return state.colorProfile.id
        },
        [GETTERS.GET_CV_COLOR_PROFILE_COLORS]: (state: CvState) =>{
            return state.colorProfile.colors;
        }
    },

    actions: {

    },
}
