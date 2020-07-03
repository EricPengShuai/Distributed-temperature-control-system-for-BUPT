<template>
  <div>
    <v-nav/>
    <div class="container">
        <h1>Profile</h1>
        <p v-if="login_adminEmail==''">Please sign in for more information</p>
        <p v-else>Email: {{login_adminEmail}}</p>
    </div>
  </div>
</template>

<script>
import VNav from '../components/VNav.vue'
import { mapState } from 'vuex'

export default {
  computed:{
    ...mapState('auth',['login_adminEmail'])
  },
  components: {
    VNav
  }
}
</script>
