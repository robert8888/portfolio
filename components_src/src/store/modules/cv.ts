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
    SET_CV_INIT_COLOR_PROFILE: 'Set_init_color_profile',

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
    state: (): CvState => ({
        colorProfile: null,
        templatedId: '',
        recruiter: {} as Recruiter,
        step: PROCESS_STEP.Configuration,
    } as CvState),

    mutations: {
        [MUTATIONS.SET_CV_COLOR_PROFILE](state: CvState, payload: ColorProfile): void{
            state.colorProfile = {
                id: payload.id,
                colors: payload.colors
            }
        },
        [MUTATIONS.SET_CV_TEMPLATE_ID](state: CvState, payload: {id: string}): void{
            state.templatedId = payload.id;
        },

        [MUTATIONS.SET_CV_RECRUITER_DATA](state: CvState, payload: Recruiter): void {
            state.recruiter = payload
        },

        [MUTATIONS.SET_CV_PROCESS_STEP](state: CvState, payload: {step: PROCESS_STEP}): void {
            state.step = payload.step;
        }
    },


    getters: {
        [GETTERS.GET_CV_TEMPLATE_ID]: (state: CvState): string | undefined => {
           return state.templatedId
        },
        [GETTERS.GET_CV_COLOR_PROFILE_ID]: (state: CvState): string | undefined => {
            return state.colorProfile?.id
        },
        [GETTERS.GET_CV_COLOR_PROFILE_COLORS]: (state: CvState): Record<string, string> =>{
            return state.colorProfile?.colors as Record<string, string>;
        },
        [GETTERS.GET_CV_PROCESS_STEP]: (state: CvState): PROCESS_STEP => {
            return state.step;
        },
        [GETTERS.GET_CV_REQUEST_DATA]: (state: CvState): Record<string, string> => {
           return {
               templateId: state.templatedId,
               colorProfileId: state.colorProfile?.id,
               recruiterEmail: state.recruiter.email,
               recruiterCompany: state.recruiter.company,
           } as Record<string, string>
        }
    },

    actions: {
        [ACTIONS.SET_CV_INIT_COLOR_PROFILE]: (
            {commit, state}: {commit: (commit: string, payload: ColorProfile) => void; state: CvState},
            payload: ColorProfile
        ): void =>{
            if(!state.colorProfile || !state.colorProfile.id)
                commit(MUTATIONS.SET_CV_COLOR_PROFILE, payload)
        },
        [ACTIONS.RESTART_CV_DOWNLOAD_PROCESS]: (
            {commit}: {commit: (commit: string, payload: {step: PROCESS_STEP}) => void}
        ): void =>{
            commit(MUTATIONS.SET_CV_PROCESS_STEP, {step: PROCESS_STEP.Configuration})
        },
        [ACTIONS.CONFIRM_TEMPLATE_CONFIG]: (
            {commit, state}: {commit: (commit: string, payload: {step: PROCESS_STEP}) => void; state: CvState}
        ): void =>{
            if(!state.colorProfile?.id || !state.templatedId)
                return
            commit(MUTATIONS.SET_CV_PROCESS_STEP, {step: PROCESS_STEP.Identification})
        },

        [ACTIONS.CONFIRM_RECRUITER]: (
            {commit}: {commit: (mutation: string, payload: Recruiter | {step: PROCESS_STEP}) => void},
            payload: {email: string; company: string}
        ): void => {
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
