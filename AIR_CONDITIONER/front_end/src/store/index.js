import Vue from "vue";
import Vuex from "vuex";

import rooms from "./rooms.module";
import center from "./center.module";
import auth from './auth.module';
import form from "./form.module"

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        rooms,
        center,
        auth,
        form
    }
});
