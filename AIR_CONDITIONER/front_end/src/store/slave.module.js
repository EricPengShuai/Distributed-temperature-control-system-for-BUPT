const api = 'http://127.0.0.1:5000/slave/'

const axios = require('axios');

export default {
    getters: {
        roomId(_, __, rootState){
            return rootState.auth.login_roomId
        },
        slave(_, getters, rootState){
            return rootState.rooms.rooms.data[getters.roomId];
        }
    },

    actions: {
        flipPower({ commit, getters, dispatch }){
            commit('rooms/set_loading', true, { root: true });
            return axios.post(api + 'flipPower', { id: getters.roomId })
                .then((room) => {
                    commit('rooms/update_id_room', {id:getters.roomId, room:room}, { root: true });
                    commit('rooms/set_loading', false, { root: true });
                    dispatch('rooms/getRooms', null,{ root: true });
                })
        },
        temp_add({ commit, getters, dispatch }, offset){
            commit('rooms/set_loading', true, { root: true });
            return axios.post(api + 'temp_add', { id: getters.roomId,offset:offset })
                .then((room) => {
                    commit('rooms/update_id_room', { id: getters.roomId, room: room }, { root: true });
                    commit('rooms/set_loading', false, { root: true });
                    dispatch('rooms/getRooms', null, { root: true });
                })
        },
        set_speed({ commit, getters, dispatch }, speed){
            commit('rooms/set_loading', true, { root: true });
            return axios.post(api + 'set_speed', { id: getters.roomId, speed: speed })
                .then((room) => {
                    commit('rooms/update_id_room', { id: getters.roomId, room: room }, { root: true });
                    commit('rooms/set_loading', false, { root: true });
                    dispatch('rooms/getRooms', null, { root: true });
                })
        },
    },
    namespaced: true,
};
