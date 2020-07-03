<template>
  <div>
    <v-nav />
    <div class="container">
      <h1>Sign In</h1>
      <div>
        <b-tabs content-class="mt-3">
          <b-tab title="Customer" active>
            <b-form>
              <b-form-group id="input-group-1" label="Room number:" label-for="input-1">
                <b-form-input
                  id="input-1"
                  v-model="roomId"
                  type="number"
                  required
                  placeholder="Enter room number"
                ></b-form-input>
              </b-form-group>

              <b-form-group id="input-group-2" label="ID card number:" label-for="input-2">
                <b-form-input
                  id="input-2"
                  v-model="idCard"
                  type="number"
                  required
                  placeholder="Enter ID card number"
                ></b-form-input>
              </b-form-group>

              <b-alert :show="error!=''" variant="danger">{{ error }}</b-alert>

              <b-button-group>
                <b-button @click="login" variant="primary">Submit</b-button>
                <b-button @click="onReset" variant="danger">Reset</b-button>
              </b-button-group>
            </b-form>
          </b-tab>
          <b-tab title="Admin">
            <b-form>
              <b-form-group id="input-group-3" label="Email address:" label-for="input-3">
                <b-form-input
                  id="input-3"
                  v-model="adminEmail"
                  type="email"
                  required
                  placeholder="Enter email"
                ></b-form-input>
              </b-form-group>

              <b-form-group id="input-group-4" label="Password:" label-for="input-4">
                <b-form-input
                  id="input-4"
                  v-model="password"
                  type="password"
                  required
                  placeholder="Enter password"
                ></b-form-input>
              </b-form-group>

              <b-alert :show="error!=''" variant="danger">{{ error }}</b-alert>

              <b-button-group>
                <b-button @click="loginAdmin" variant="primary">Submit</b-button>
                <b-button @click="onReset" variant="danger">Reset</b-button>
              </b-button-group>
            </b-form>
          </b-tab>
        </b-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import VNav from "../components/VNav.vue";
import { mapState, mapActions } from "vuex";

export default {
  components: {
    VNav
  },
  computed: {
    ...mapState("auth", [
      "roomId",
      "idCard",
      "adminEmail",
      "password",
      "login_roomId",
      "login_adminEmail",
      "error"
    ]),
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
    roomId: {
      get() {
        return this.$store.roomId;
      },
      set(value) {
        this.$store.commit("auth/set_roomId", value);
      }
    },
    idCard: {
      get() {
        return this.$store.idCard;
      },
      set(value) {
        this.$store.commit("auth/set_idCard", value);
      }
    }
  },
  watch: {
    login_roomId: function() {
      this.$router.push("/Home");
    },
    login_adminEmail: function() {
      this.$router.push("/Home");
    }
  },
  methods: {
    ...mapActions("auth", ["loginAdmin", "login"]),
    onReset() {
      this.$store.commit("auth/set_error", "");
    }
  },
  created() {
    this.onReset();
  }
};
</script>