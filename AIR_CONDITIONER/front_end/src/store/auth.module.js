const api = 'http://127.0.0.1:5000/auth/'

const axios = require('axios');

export default {
    state: {
        roomId: '',
        login_roomId: '',
        idCard: '',
        adminEmail: '',
        login_adminEmail: '',
        password: '',
        loading: false,
        error: '',
    },

    getter: {
        adminHaveLogin(state) {
            return state.adminEmail != null;
        },
        haveLogin(state) {
            return state.roomId != null;
        }
    },

    mutations: {
        set_roomId(state, roomId) {
            state.roomId = roomId;
        },
        set_login_roomId(state, roomId) {
            state.login_roomId = roomId;
        },
        set_idCard(state, idCard) {
            state.idCard = idCard;
        },
        set_adminEmail(state, adminEmail) {
            state.adminEmail = adminEmail;
        },
        set_login_adminEmail(state, adminEmail) {
            state.login_adminEmail = adminEmail;
        },
        set_password(state, password) {
            state.password = password;
        },
        set_loading(state, loading) {
            state.loading = loading;
        },
        set_error(state, error) {
            state.error = error;
        },
        set_success(state, success) {
            state.success = success;
        },
    },

    actions: {
        register({ commit, state }) {
            commit('set_loading', true);
            return axios.post(api + 'register', { email: state.adminEmail, pwd: state.password })
                .then((rep) => {
                    if (rep.data.error == true) {
                        commit('set_loading', false)
                        commit('set_error', "Register Failed: This email has been registered!")
                    }
                    else {
                        commit('set_loading', false)
                        commit('set_error', "")
                        commit('set_login_adminEmail', state.adminEmail)

                    }
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        loginAdmin({ commit, state }) {
            commit('set_loading', true);
            return axios.post(api + 'loginAdmin', { email: state.adminEmail, pwd: state.password })
                .then((rep) => {
                    if (rep.data.error == true) {
                        commit('set_loading', false)
                        commit('set_error', "This email doesn't exist or password wrong!")
                    }
                    else {
                        commit('set_login_adminEmail', state.adminEmail)
                        commit('set_loading', false)
                        commit('set_error', "")
                    }
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        login({ commit, state }) {
            commit('set_loading', true);
            return axios.post(api + 'login', { roomId: state.roomId, idCard: state.idCard })
                .then((rep) => {
                    if (rep.data.error == true) {
                        commit('set_loading', false)
                        commit('set_error', "This room does't in range or id card number wrong!")
                    }
                    else {
                        commit('set_login_roomId', state.roomId)
                        commit('set_loading', false)
                        commit('set_error', "")
                    }
                })
                .catch((error) => {
                    console.error(error)
                })
        },
    },
    namespaced: true,
};
