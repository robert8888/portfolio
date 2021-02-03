
export interface CounterState {
   value: number;
}

export const MUTATIONS = {
    INCREMENT: "increment",
    DECREMENT: "decrement"
}

export const ACTIONS = {

}

export const GETTERS = {

}

export default {
    state: () => ({
        value: 0
    }),
    mutations: {
       [MUTATIONS.INCREMENT](state: CounterState, delta: number) {
          state.value += delta
       },
        [MUTATIONS.DECREMENT](state: CounterState, delta: number) {
            state.value -= delta
       }
    },
    actions: {

    },
    getters: {

    }
}
