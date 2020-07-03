<template>
  <div>
    <v-nav />
    <br />
    <div v-if="login_roomId==''||this.rooms.data[ this.roomId].idCard==''" class="container">
      <h1>Room</h1>
      <p>Please sign in for more information</p>
    </div>
    <div v-else class="container">
      <v-center admin="false" />
      <br />
      <v-slave :roomId="roomId" />
      <!-- User info -->
      <b-card
        :title="'Hope you feel at home. Welcome ' + this.rooms.data[ this.roomId].name + '!'"
        header-tag="header"
        bg-variant="light"
      >
        <template v-slot:header>
          <h6 class="mb-0">User Panel</h6>
        </template>
        <p>Your ID Card Number: {{ this.rooms.data[ this.roomId].idCard }}</p>
        <p>Your Check In Date: {{ this.rooms.data[ this.roomId].checkInDate }}</p>
        <p>Is Running : {{ this.rooms.data[ this.roomId].is_blowing_in }}</p>
        <p>Your Cost : {{ this.rooms.data[ this.roomId].cost }}</p>
        <p>Energy : {{ this.rooms.data[this.roomId].cost/5 }}</p>
      </b-card>
    </div>
  </div>
</template>

<script>
import VNav from "../components/VNav.vue";
import VSlave from "../components/VSlave.vue";
import VCenter from "../components/VCenter.vue";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("auth", ["login_roomId"]),
    ...mapState("rooms", ["rooms"]),
    roomId() {
      return parseInt(this.login_roomId);
    }
  },
  components: {
    VNav,
    VCenter,
    VSlave
  }
};
</script>