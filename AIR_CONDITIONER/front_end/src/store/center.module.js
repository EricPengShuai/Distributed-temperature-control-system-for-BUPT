const api = 'http://127.0.0.1:5000/center/'

const axios = require('axios');

export default {
    state: {
        power: false,
        state: 'Standby',
        mode: 'Cold',
        temp: 25,
		freq: 10
    },

    mutations: {
        set_center(state, center) {
            state.power = center.power;
            state.state = center.state;
            state.mode = center.mode;
            state.temp = center.temp;
			state.freq = center.freq;
        },
    },

    actions: {
        socket_getCenter({ commit }, center) {
            commit('set_center', center)
        },
        flipPower() {
            return axios.post(api + 'flipPower')
        },
        setMode(_, mode) {
            return axios.post(api + 'setMode', { mode: mode })
        },
        temp_add(_, offset) {
            return axios.post(api + 'temp_add', { offset: offset })
        },
		freq_add(_,offset){
			return axios.post(api + 'freq_add',{offset:offset});
		}
    },
    namespaced: true,
};
