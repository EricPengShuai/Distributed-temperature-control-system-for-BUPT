<template>
	<div class="container">
		<b-overlay :show="loading" rounded="sm">
			<b-card title="Center" header-tag="header" bg-variant="light">
				<template v-slot:header>
					<h6 class="mb-0">Air Conditioning Panel</h6>
				</template>

				<b-button :variant="power ? 'outline-danger':'outline-info'" v-if="admin=='true'" @click="flipPower" class="mb-2"
				size="sm">
					<b-icon icon="power" aria-hidden="true"></b-icon>
					{{ power ? "Power Off":"Power On" }}
				</b-button>
				<b-button-toolbar size="sm" v-if="power">
					<b-button-group size="sm" class="mb-1">
						<b-button variant="outline-primary" disabled>State</b-button>
						<b-button :variant="state=='Standby'?'outline-secondary':'outline-success'" disabled>{{ state }}</b-button>
					</b-button-group>
					<b-button-group size="sm" class="mb-1 ml-1">
						<b-button variant="outline-warning" disabled>Mode</b-button>
						<b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" disabled>{{ mode }}</b-button>
					</b-button-group>
					<b-button-group size="sm" class="mb-1 ml-1" right>
						<b-button variant="outline-success" disabled>Temperature</b-button>
						<b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" disabled>{{ temp }}</b-button>
					</b-button-group>
					<b-button-group size="sm" class="mb-1 ml-1" right>
						<b-button variant="outline-success" disabled>Frequency</b-button>
						<b-button variant="outline-success" disabled>{{ freq }}</b-button>
					</b-button-group>
				</b-button-toolbar>
				<b-button size="sm" v-b-toggle.setting v-if="power && admin=='true'" variant="outline-secondary">
					<b-icon icon="gear-fill" aria-hidden="true"></b-icon>Settings
				</b-button>
				<b-collapse id="setting" class="mt-2" v-if="power">
					<b-button-toolbar size="sm">
						<b-button-group size="sm">
							<b-dropdown size="sm" variant="outline-warning" right text="Mode">
								<b-dropdown-item variant="outline-info" @click="setCold">Cold</b-dropdown-item>
								<b-dropdown-divider></b-dropdown-divider>
								<b-dropdown-item variant="outline-danger" @click="setHot">Hot</b-dropdown-item>
							</b-dropdown>
						</b-button-group>
						<b-button-group size="sm" class="ml-1" right>
							<b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" @click="temp_up">
								<b-icon icon="arrow-up"></b-icon>
							</b-button>
							<b-button variant="outline-success" disabled>Temperature</b-button>
							<b-button :variant="mode=='Cold'?'outline-info':'outline-danger'" @click="temp_down">
								<b-icon icon="arrow-down"></b-icon>
							</b-button>
						</b-button-group>
						<b-button-group size="sm" class="ml-1" right>
							<b-button variant="outline-success" @click="freq_up">
								<b-icon icon="arrow-up"></b-icon>
							</b-button>
							<b-button variant="outline-success" disabled>Frequency</b-button>
							<b-button variant="outline-success" @click="freq_down">
								<b-icon icon="arrow-down"></b-icon>
							</b-button>
						</b-button-group>
					</b-button-toolbar>
				</b-collapse>
			</b-card>
		</b-overlay>
	</div>
</template>

<script>
	import Vuex from "vuex";

	const mapState = Vuex.mapState;
	const mapActions = Vuex.mapActions;

	export default {
		props: {
			admin: String
		},
		computed: {
			...mapState("center", ["power", "state", "mode", "temp", "freq", "loading"]),
			...mapState("rooms", ["rooms"]),
			state() {
				for(var i = 0; i < this.rooms.data.length; i++){
					if(this.rooms.data[i].is_blowing_in)
						return 'working';
				}
				return 'Standby'
			}
		},
		methods: {
			...mapActions("center", ["flipPower", "setMode", "temp_add", "freq_add"]),
			setCold() {
				if (this.mode == "Cold") return;
				return this.setMode("Cold");
			},
			setHot() {
				if (this.mode == "Hot") return;
				return this.setMode("Hot");
			},
			temp_up() {
				if (this.mode == "Cold") {
					if (this.temp == 25) return;
					return this.temp_add(1);
				}
				if (this.temp == 30) return;
				return this.temp_add(1);
			},
			temp_down() {
				if (this.mode == "Cold") {
					if (this.temp == 18) return;
					return this.temp_add(-1);
				}
				if (this.temp == 25) return;
				return this.temp_add(-1);
			},
			freq_up(){
				return this.freq_add(5);
			},
			freq_down(){
				return this.freq_add(-5);
			}
		},
		created() {
			this.$socket.client.emit("update_center");
		}
	};
</script>
