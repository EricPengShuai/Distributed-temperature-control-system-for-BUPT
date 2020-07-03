<template>
  <div>
    <div class="container">
      <!-- Air Conditioning Info -->
      <b-card
        :title="'Room ' +  this.roomId + ' Air Conditioning'"
        header-tag="header"
        bg-variant="light"
      >
        <template v-slot:header>
          <h6 class="mb-0">Air Conditioning Panel</h6>
        </template>

        <b-button-toolbar size="sm">
          <b-button-group size="sm" class="mb-1" right>
            <b-button variant="outline-success" disabled>Temperature Now</b-button>
            <b-button
              :variant="this.rooms.data[ this.roomId].temp<25?'outline-info':'outline-danger'"
              disabled
            >{{ this.rooms.data[ this.roomId].temp }}</b-button>
          </b-button-group>
        </b-button-toolbar>

        <b-button
          :variant="this.rooms.data[ this.roomId].power ? 'outline-danger':'outline-info'"
          @click="flipPower(roomId)"
          class="mb-2"
          size="sm"
        >
          <b-icon icon="power" aria-hidden="true"></b-icon>
          {{ this.rooms.data[ this.roomId].power ? "Power Off":"Power On" }}
        </b-button>

        <b-button-toolbar size="sm" v-if="this.rooms.data[ this.roomId].power">
          <b-button-group size="sm" class="mb-1" right>
            <b-button variant="outline-success" disabled>Temperature Set</b-button>
            <b-button
              :variant="this.rooms.data[ this.roomId].expectTemp<25?'outline-info':'outline-danger'"
              disabled
            >{{ this.rooms.data[ this.roomId].expectTemp }}</b-button>
          </b-button-group>
          <b-button-group size="sm" class="mb-1 ml-1">
            <b-button variant="outline-primary" disabled>Speed</b-button>
            <b-button
              :variant="this.rooms.data[ this.roomId].speed=='High'?'outline-warning':'outline-success'"
              disabled
            >{{ this.rooms.data[ this.roomId].speed }}</b-button>
          </b-button-group>
        </b-button-toolbar>

        <b-button
          size="sm"
          v-b-toggle.setting_slave
          v-if="this.rooms.data[ this.roomId].power"
          variant="outline-secondary"
        >
          <b-icon icon="gear-fill" aria-hidden="true"></b-icon>Settings
        </b-button>
        <b-collapse id="setting_slave" class="mt-2" v-if="this.rooms.data[ this.roomId].power">
          <b-button-toolbar size="sm">
            <b-button-group size="sm" right>
              <b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" @click="temp_up">
                <b-icon icon="arrow-up"></b-icon>
              </b-button>
              <b-button variant="outline-success" disabled>Temperature</b-button>
              <b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" @click="temp_down">
                <b-icon icon="arrow-down"></b-icon>
              </b-button>
            </b-button-group>

            <b-button-group size="sm" class="ml-1" right>
              <b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" @click="speed_up">
                <b-icon icon="arrow-up"></b-icon>
              </b-button>
              <b-button variant="outline-primary" disabled>Speed</b-button>
              <b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" @click="speed_down">
                <b-icon icon="arrow-down"></b-icon>
              </b-button>
            </b-button-group>
          </b-button-toolbar>
        </b-collapse>
      </b-card>
      <br />
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  props: {
    roomId: Number
  },
  computed: {
    ...mapState("rooms", ["rooms"]),
    ...mapState("center", ["mode"])
  },
  methods: {
    ...mapActions("rooms", ["temp_add", "set_speed", "flipPower"]),
    temp_up() {
      if (this.mode == "Cold") {
        if (this.rooms.data[this.roomId].expectTemp == 25) return;
        return this.temp_add({ id: this.roomId, offset: 1 });
      }
      if (this.rooms.data[this.roomId].expectTemp == 30) return;
      return this.temp_add({ id: this.roomId, offset: 1 });
    },
    temp_down() {
      if (this.mode == "Cold") {
        if (this.rooms.data[this.roomId].expectTemp == 18) return;
        return this.temp_add({ id: this.roomId, offset: -1 });
      }
      if (this.rooms.data[this.roomId].expectTemp == 25) return;
      return this.temp_add({ id: this.roomId, offset: -1 });
    },
    speed_up() {
      if (this.rooms.data[this.roomId].speed == "Low")
        return this.set_speed({ id: this.roomId, speed: "Mid" });
      if (this.rooms.data[this.roomId].speed == "Mid")
        return this.set_speed({ id: this.roomId, speed: "High" });
    },
    speed_down() {
      if (this.rooms.data[this.roomId].speed == "High")
        return this.set_speed({ id: this.roomId, speed: "Mid" });
      if (this.rooms.data[this.roomId].speed == "Mid")
        return this.set_speed({ id: this.roomId, speed: "Low" });
    }
  }
};
</script>