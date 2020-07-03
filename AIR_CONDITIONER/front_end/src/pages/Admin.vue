<template>
  <div>
    <v-nav />
    <div v-if="login_adminEmail==''" class="container">
      <h1>Admin Page</h1>
      <p>Please sign in for more information</p>
    </div>
    <div v-else>
      <br />
      <v-center admin="true" />
      <br />
      <div class="container" v-if="power">
        <h1>Rooms:</h1>
        <b-table :items="rooms.data" :fields="fields" striped responsive="sm">
          <template v-slot:cell(show_details)="row">
            <b-button
              size="sm"
              @click="flipShow(row.index);row.toggleDetails"
              class="mr-2"
            >{{ row.detailsShowing ? 'Hide' : 'Show'}} Details</b-button>
          </template>

          <template v-slot:row-details="details">
            <b-form>
              <b-form-group id="input-group-1" label="ID card number:" label-for="input-1">
                <b-form-input
                  id="input-1"
                  v-model="details.item.idCard"
                  type="number"
                  required
                  placeholder="Enter ID card number"
                ></b-form-input>
              </b-form-group>

              <b-form-group id="input-group-2" label="Name:" label-for="input-2">
                <b-form-input
                  id="input-1"
                  v-model="details.item.name"
                  type="text"
                  required
                  placeholder="Enter name"
                ></b-form-input>
              </b-form-group>

              <v-slave :roomId="parseInt(details.item.id)" v-if="details.item.haveCheckIn" />

              <b-button-group>
                <b-button
                  v-if="!details.item.haveCheckIn"
                  @click="checkIn(details.item)"
                  variant="primary"
                >Check In</b-button>
                <b-button v-else @click="checkOut(details.item)" variant="danger">Check Out</b-button>
              </b-button-group>
            </b-form>
          </template>
        </b-table>
      </div>
    </div>
  </div>
</template>

<script>
import VNav from "../components/VNav.vue";
import VCenter from "../components/VCenter.vue";
import Vuex from "vuex";
import VSlave from "../components/VSlave.vue";

const mapState = Vuex.mapState;
const mapActions = Vuex.mapActions;

export default {
  data() {
    return {
      fields: [
        "id",
        "name",
        "checkInDate",
        "cost",
        "is_blowing_in",
        "expectTemp",
        "speed",
        "temp",
        "show_details"
      ]
    };
  },
  computed: {
    ...mapState("auth", ["login_adminEmail"]),
    ...mapState("rooms", ["rooms"]),
    ...mapState("center", ["power"])
  },
  methods: {
    ...mapActions("rooms", ["checkIn", "checkOut", "flipShow", "updateRooms"])
  },
  watch: {
    rooms: {
      handler: function(to) {
        this.updateRooms(to.data);
      },
      deep: true
    }
  },
  components: {
    VCenter,
    VNav,
    VSlave
  },
  created() {
    this.$socket.client.emit("update_rooms");
  }
};
</script>