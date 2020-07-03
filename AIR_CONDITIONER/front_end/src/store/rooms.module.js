const api = 'http://127.0.0.1:5000/rooms/'

const axios = require('axios');

export default {
    state: {
        rooms: [],
    },

    mutations: {
        update_rooms(state, rooms) {
            // 为了使其动态更新，添加something无用量
            var something = { data: rooms }
            state.rooms = something;
        },
    },

    actions: {
        socket_getRooms({ commit }, rooms) {
            commit('update_rooms', rooms)
        },
        checkIn(_, room) {
            return axios.post(api + 'checkIn', room)
        },
        checkOut(_, room) {
            return axios.post(api + 'checkOut', room)
        },
        flipPower(_, roomId) {
            return axios.post(api + 'flipPower', { id: roomId })
        },
        temp_add(_, payload) {
            return axios.post(api + 'temp_add', payload)
        },
        set_speed(_, payload) {
            return axios.post(api + 'set_speed', payload)
        },
        flipShow(_, roomId) {
            return axios.post(api + 'flipShow', { id: roomId })
        },
        updateRooms(_, rooms) {
            return axios.post(api + 'updateRooms', rooms)
        }
    },
    namespaced: true,
};
