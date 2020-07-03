<template>
  <div>
    <v-nav />
    <b-overlay :show="loading" rounded="sm">
      <div class="container">
        <h1>Sign Up</h1>
        <div>
          <b-alert show variant="warning">Notice that only administrator can sign up an account!</b-alert>
          <b-alert show variant="info">
            Customer? click
            <a href="#/login">here</a> to sign in right now.
          </b-alert>
        </div>
        <b-form>
          <b-form-group
            id="input-group-1"
            label="Email address:"
            label-for="input-1"
            description="We'll never share your email with anyone else."
          >
            <b-form-input
              id="input-1"
              v-model="adminEmail"
              type="email"
              required
              placeholder="Enter email"
            ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-2" label="Password:" label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="password"
              type="password"
              required
              placeholder="Enter password"
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-4"
            label="Admin Code:"
            label-for="input-4"
            description="This is used to verify the identity of the administrator"
          >
            <b-form-input
              id="input-4"
              v-model="adminCode"
              :state="checkCode"
              type="password"
              aria-describedby="input-live-help input-live-feedback"
              required
              placeholder="Enter admin code"
            ></b-form-input>
            <b-form-invalid-feedback id="input-live-feedback">Admin Code Wrong</b-form-invalid-feedback>
          </b-form-group>

          <b-alert :show="error!=''" variant="danger">{{ error }}</b-alert>

          <b-button-group>
            <b-button @click="register" variant="primary" :disabled="!checkCode">Submit</b-button>
            <b-button @click="onReset" variant="danger">Reset</b-button>
          </b-button-group>
        </b-form>
      </div>
    </b-overlay>
  </div>
</template>

<script>
import VNav from "../components/VNav.vue";
import Vuex from "vuex";

const mapState = Vuex.mapState;

export default {
  components: {
    VNav
  },
  data() {
    return {
      adminCode: ""
    };
  },
  computed: {
    ...mapState("auth", ["login_adminEmail", "error", "loading"]),
    adminEmail: {
      get() {
        return this.$store.adminEmail;
      },
      set(value) {
        this.$store.commit("auth/set_adminEmail", value);
      }
    },
    password: {
      get() {
        return this.$store.password;
      },
      set(value) {
        this.$store.commit("auth/set_password", value);
      }
    },
    checkCode() {
      return this.adminCode == "vue";
    }
  },
  watch: {
    login_adminEmail: function() {
      this.$router.push("/Home");
    }
  },
  methods: {
    register() {
      this.$store.dispatch("auth/register");
      this.adminCode = "";
    },
    onReset() {
      this.adminEmail = "";
      this.password = "";
      this.adminCode = "";
      this.$store.commit("auth/set_error", "");
    }
  },
  created() {
    this.onReset();
  }
};
</script>