import {getProjects} from "@/api/backend_api";

interface Project {
    name: string;
    type: string;
    typeValue: string;
    title: string;
    subtitle: string;
    description: string;
    technologies: {
        color: string;
        name: string;
        link: string;
        isHighlighted: boolean;
    }[];
    images: {
        url: string;
        height: number;
        width: number;
    }[];
}

interface Status{
    loading: boolean;
    success: boolean;
    errors: string[];
}

export interface ProjectsState {
    filter: Map<string, string[]>;
    order: {
        value: string;
        param: string;
    };
    infinityScroll: {
        offset: number;
        limit: number;
        chunk: number;
        startLimit: number;
        count: number;
    };
    projects: Project[];
    status: Status;
}

export const MUTATIONS = {
    SET_FILTER_VALUE: "set_projects_filter_value",
    SET_ORDER: 'set_projects_order',

    SET_INF_SCROLL_NEXT_LIMIT: 'set_inf-scroll_next_chunk_limit',
    SET_INF_SCROLL_COUNT_LIMIT: 'set_inf-scroll_count_limit',
    RESET_INF_SCROLL: 'set_initial_state_inf-scroll',

    SET_PROJECTS: 'set-projects',
    SET_STATUS_LOADING: 'set-status-loading',
    SET_STATUS_RESULTS: 'set-status-results',
}

export const ACTIONS = {
    UPDATE_FILTER: 'update_projects_filtering',
    UPDATE_ORDER: 'update_projects_order',
    FETCH_PROJECTS: 'fetching_projects',
}

export const GETTERS = {
    GET_FILTER_VALUE: 'get_current_filter_values',
    GET_ORDER: 'get_current_order_value',
    GET_PROJECTS: 'get_current_projects',
    GET_STATUS: 'get_current_status',
}

export default {
    state: () => ({
        filter: new Map<string, string[]>(),
        order: {
            value: "",
            param: "",
        },
        infinityScroll: {
            offset: 0,
            limit: 0,
            chunk: 6,
            startLimit: 12,
            count: 0,
        },
        projects: [],
        status: {
            loading: false,
            success: true,
            errors: [],
        }
    } as ProjectsState),

    mutations: {
        [MUTATIONS.SET_FILTER_VALUE]: (state: ProjectsState, payload: {type: string; value: string | string[] }) => {
            if(typeof payload.value === 'string')
                    payload.value = [payload.value]
            state.filter.set(payload.type, payload.value)
        },
        [MUTATIONS.SET_ORDER]: (state: ProjectsState, {value, param}: {value: string; param: string}) => {
            state.order.value = value;
            state.order.param = param;
        },
        [MUTATIONS.SET_INF_SCROLL_NEXT_LIMIT]:(state: ProjectsState) => {
            const chunk = state.infinityScroll.chunk;
            state.infinityScroll.offset += chunk;
            state.infinityScroll.limit += chunk;
        },
        [MUTATIONS.SET_INF_SCROLL_COUNT_LIMIT]: (state: ProjectsState, payload: {count: number}) => {
            state.infinityScroll.count = payload.count;
        },
        [MUTATIONS.RESET_INF_SCROLL]: (state: ProjectsState) => {
            state.infinityScroll.offset = 0;
            state.infinityScroll.limit = 0;
        },
        [MUTATIONS.SET_PROJECTS]: (state: ProjectsState, payload: Project[]) => {
            state.projects = payload;
        },
        [MUTATIONS.SET_STATUS_LOADING]: (state: ProjectsState, payload: boolean) => {
            state.status.loading = payload;
        },
        [MUTATIONS.SET_STATUS_RESULTS]: (state: ProjectsState, payload: Status) => {
            state.status = payload;
        },
    },

    getters: {
        [GETTERS.GET_FILTER_VALUE]: (state: ProjectsState) => (type: string) => {
            return state.filter.get(type);
        },
        [GETTERS.GET_ORDER]: (state: ProjectsState) => {
            return state.order;
        },
        [GETTERS.GET_PROJECTS]: (state: ProjectsState) => {
            return state.projects;
        },
        [GETTERS.GET_STATUS]: (state: ProjectsState) => {
            return state.status;
        },
    },

    actions: {
        async [ACTIONS.FETCH_PROJECTS](
            { commit, state }: {commit: Function; state: ProjectsState},
        ){
            commit(MUTATIONS.SET_STATUS_LOADING, true)
            const data = {} as Record<string, any>
            state.filter.forEach((value, key) => {
                data[key] = value.join(",")
            })
            data[state.order.param] = state.order.value
            try{
                const response = await getProjects(data)
                console.log('fetching projects', response.data)
                if(response.success){
                    commit(MUTATIONS.SET_PROJECTS, response.data as Project[])
                } else
                    commit(MUTATIONS.SET_STATUS_RESULTS, {
                        success: false,
                        error: [
                            'Search projects api error'
                        ],
                        loading: false,
                    })
            } catch {
                commit(MUTATIONS.SET_STATUS_RESULTS, {
                    success: false,
                    error: [
                        'Api connection error'
                    ],
                    loading: false,
                })
            } finally {
                commit(MUTATIONS.SET_STATUS_LOADING, false)
            }
        },
        [ACTIONS.UPDATE_FILTER]({ commit }: {commit: Function}, payload: {type: string; value: string[] | number[] | string}){
            commit(MUTATIONS.SET_FILTER_VALUE, payload);
        },
        [ACTIONS.UPDATE_ORDER]({ commit }: {commit: Function}, payload: {index: number}){
            commit(MUTATIONS.SET_ORDER, payload)
        },
    },
}
