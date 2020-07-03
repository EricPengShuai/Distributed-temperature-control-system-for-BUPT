<template>
  <div>
    <v-nav />
    <div class="container">
      <h1>Home</h1>
      <p v-if="login_adminEmail==''">Please sign in for more information</p>
      <p v-else>Welcome {{login_adminEmail}}</p>
    </div>
  </div>
</template>

<script>
import VNav from "../components/VNav.vue";
import { mapState } from "vuex";

export default {
  name: "Home",
  computed: {
    ...mapState("auth", ["login_adminEmail"])
  },
  components: {
    VNav
  }
};
</script>
