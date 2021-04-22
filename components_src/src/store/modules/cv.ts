export interface ColorProfile{
    id: string;
    colors: {
        [key: string]: string;
    };
}

export interface Recruiter{
    email: string;
    company?: string;
}

export enum PROCESS_STEP{
    Configuration = 'conf',
    Identification = 'ident',
    Download = 'download'
}

export interface CvState {
    colorProfile: ColorProfile | null;
    templatedId: string;
    recruiter: Recruiter;
    step: PROCESS_STEP;
}

export const MUTATIONS = {
    SET_CV_COLOR_PROFILE_ID: 'set_color_profile_id',
    SET_CV_COLOR_PROFILE: 'Set_color_profile',
    SET_CV_TEMPLATE_ID: 'Set_template_id',

    SET_CV_RECRUITER_DATA: 'set_cv_recruiter_profile_data',

    SET_CV_PROCESS_STEP: 'set_cv_process_step'
}

export const ACTIONS = {
    CONFIRM_TEMPLATE_CONFIG: 'confirm_template_configuration',
    CONFIRM_RECRUITER: 'config_recruiter_data',
    RESTART_CV_DOWNLOAD_PROCESS: 'set_initial_step',
}

export const GETTERS = {
    GET_CV_TEMPLATE_ID: "get_template_id",
    GET_CV_COLOR_PROFILE_ID: "get_color_profile_id",
    GET_CV_COLOR_PROFILE_COLORS: "get_color_profile_colors",

    GET_CV_PROCESS_STEP: "get_cv_download_process_step",
    GET_CV_REQUEST_DATA: 'get_cv_download_required_data',
}

export default {
    state: () => ({
        colorProfile: null,
        templatedId: '',
        recruiter: {} as Recruiter,
        step: PROCESS_STEP.Configuration,
    } as CvState),

    mutations: {
        [MUTATIONS.SET_CV_COLOR_PROFILE](state: CvState, payload: {id: string; colors: Record<string, string>}){
            state.colorProfile = {
                id: payload.id,
                colors: payload.colors
            }
        },

        [MUTATIONS.SET_CV_TEMPLATE_ID](state: CvState, payload: {id: string}){
            state.templatedId = payload.id;
        },

        [MUTATIONS.SET_CV_RECRUITER_DATA](state: CvState, payload: Recruiter){
            state.recruiter = payload
        },

        [MUTATIONS.SET_CV_PROCESS_STEP](state: CvState, payload: {step: PROCESS_STEP}){
            state.step = payload.step;
        }
    },


    getters: {
        [GETTERS.GET_CV_TEMPLATE_ID]: (state: CvState) => {
           return state.templatedId
        },
        [GETTERS.GET_CV_COLOR_PROFILE_ID]: (state: CvState) => {
            return state.colorProfile?.id
        },
        [GETTERS.GET_CV_COLOR_PROFILE_COLORS]: (state: CvState) =>{
            return state.colorProfile?.colors;
        },
        [GETTERS.GET_CV_PROCESS_STEP]: (state: CvState) => {
            return state.step;
        },
        [GETTERS.GET_CV_REQUEST_DATA]: (state: CvState) => {
           return {
               templateId: state.templatedId,
               colorProfileId: state.colorProfile?.id,
               recruiterEmail: state.recruiter.email,
               recruiterCompany: state.recruiter.company,
           }
        }
    },

    actions: {
        [ACTIONS.RESTART_CV_DOWNLOAD_PROCESS]: ({commit}: {commit: Function}) =>{
            commit(MUTATIONS.SET_CV_PROCESS_STEP, {step: PROCESS_STEP.Configuration})
        },
        [ACTIONS.CONFIRM_TEMPLATE_CONFIG]: ({commit, state}: {commit: Function; state: CvState}) =>{
            if(!state.colorProfile?.id || !state.templatedId)
                return
            commit(MUTATIONS.SET_CV_PROCESS_STEP, {step: PROCESS_STEP.Identification})
        },

        [ACTIONS.CONFIRM_RECRUITER]: ({commit}: {commit: Function}, payload: {email: string; company: string}) => {
            commit(MUTATIONS.SET_CV_RECRUITER_DATA, {
                email: payload.email,
                company: payload.company
            } as Recruiter)
            if(payload.email && payload.company){
                commit(MUTATIONS.SET_CV_PROCESS_STEP, {step: PROCESS_STEP.Download})
            }
        }
    },
}
