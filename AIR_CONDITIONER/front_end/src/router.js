import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from './pages/Home';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import About from './pages/About.vue'
import Admin from './pages/Admin.vue'
import Room from './pages/Room.vue'
import Profile from './pages/Profile.vue'
import Form from './pages/Form.vue'

Vue.use(VueRouter);

export default new VueRouter({
    routes: [
        { path: '/', component: Home },
        { path: '/home', name: 'home', component: Home },
        { path: '/about', name: 'about', component: About },
        { path: '/login', name: 'login', component: Login },
        { path: '/register', name: 'register', component: Register },
        { path: '/admin', name: 'admin', component: Admin },
        { path: '/room', name: 'room', component: Room },
        { path: '/profile', name: 'profile', component: Profile },
        { path: '/form', name: 'form', component: Form }
    ]
});