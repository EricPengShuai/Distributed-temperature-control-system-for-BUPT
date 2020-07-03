<template>
  <div>
    <b-overlay :show="!isConnect" rounded="sm">
    <router-view></router-view>
    </b-overlay>
  </div>
</template>
<script>
export default {
  name: "App",
  data() {
    return {
      isConnect: false,
    }
  },
  sockets: {
    connect() {
      console.log("connect");
      this.isConnect = true;
    },
    disconnect() {
      console.log("disconnect");
      this.isConnect = false;
    },
    message(message) {
      console.log(message);
    },
    ping() {
      console.log("keep alive");
    }
  },
  mounted() {
    this.$socket.client.emit("update_rooms");
    setInterval(function(){this.$socket.client.emit("update_rooms");}.bind(this), 1000);
  }
};
</script>

<style></style>
