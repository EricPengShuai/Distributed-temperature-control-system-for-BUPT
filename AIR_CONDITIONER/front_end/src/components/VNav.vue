<template>
  <b-navbar toggleable="lg" type="light" variant="light" sticky>
    <b-navbar-brand href="#/">
      <img src="../assets/brand_icon.png" height="40" />
      Distributed temperature control system
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right v-if="adminHaveSignedIn">
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>User</template>
          <b-dropdown-item href="#/Profile">Profile</b-dropdown-item>
          <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-navbar-nav>
          <b-nav-item href="#/About">About</b-nav-item>
          <b-nav-item href="#/Form" v-if="adminHaveSignedIn">Form</b-nav-item>
          <b-nav-item href="#/Admin" v-if="adminHaveSignedIn">Admin</b-nav-item>
          <b-nav-item href="#/Room" v-if="haveSignedIn">Room</b-nav-item>
          <b-nav-item @click="logout" v-if="haveSignedIn">Sign Out</b-nav-item>
          <b-nav-item href="#/Register" v-if="didntSignedIn">Sign Up</b-nav-item>
          <b-nav-item href="#/Login" v-if="didntSignedIn">Sign In</b-nav-item>
        </b-navbar-nav>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>


<script>
import { mapState } from "vuex";
export default {
  name: "VNav",
  computed: {
    ...mapState("auth", ["login_adminEmail", "login_roomId"]),
    adminHaveSignedIn() {
      return this.login_adminEmail != "";
    },
    haveSignedIn() {
      return this.login_roomId != "";
    },
    didntSignedIn() {
      return !this.adminHaveSignedIn && !this.haveSignedIn;
    }
  },
  methods: {
    logout() {
      this.$store.commit("auth/set_login_adminEmail", "");
      this.$store.commit("auth/set_login_roomId", "");
      this.$router.push("/Home");
    }
  }
};
</script>
