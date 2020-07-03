<template>
	<div>
		<v-nav />
		<div v-if="login_adminEmail==''" class="container">
			<h1>Admin Page</h1>
			<p>Please sign in for more information</p>
		</div>
		<div v-else>
			<div>
				<b-card bg-variant="light">
					<b-form-group label-cols-lg="2" label="Form Infomation" label-size="lg" label-class="font-weight-bold pt-0" class="mb-0">
						<b-form-group label-cols-sm="2" label="Starting Date:" label-align-sm="left" label-for="sd">
							<b-form-datepicker id="sd" v-model="sd" class="mb-2"></b-form-datepicker>
						</b-form-group>
						<b-form-group label-cols-sm="2" label="Ending Date:" label-align-sm="left" label-for="ed">
							<b-form-datepicker id="ed" v-model="ed" class="mb-2"></b-form-datepicker>
						</b-form-group>
						<b-form-group label-cols-sm="2" label="Starting Room:" label-align-sm="left" label-for="sr">
							<b-form-select id='sr' v-model="sr" :options="roomList"></b-form-select>
						</b-form-group>
						<b-form-group label-cols-sm="2" label="Ending Room:" label-align-sm="left" label-for="er">
							<b-form-select id='er' v-model="er" :options="roomList"></b-form-select>
						</b-form-group>
						<b-alert show variant="warning" v-if="legal==false">You cannot get form with incomplete data!</b-alert>
						<b-row>
							<b-col>
								<b-button variant="outline-success" size="lg" @click="gf()">Submit</b-button>
							</b-col>
							<b-col>
								<b-button variant="outline-primary" size="lg" @click="df(true)" v-if="success">Download Summary</b-button>
							</b-col>
							<b-col>
								<b-button variant="outline-info" size="lg" @click="df(false)" v-if="success">Download Details</b-button>
							</b-col>
						</b-row>
					</b-form-group>
				</b-card>
				<b-overlay :show='false'>
					<b-form-group label-cols-sm="2" label="Summary:" label-for="summary">
						<b-table striped hover :items="summary" id="summary"> </b-table>
					</b-form-group>
					<b-form-group label-cols-sm="2" label="Details:" label-for="detail">
						<b-table striped hover :items="form" id="detail"></b-table>
					</b-form-group>
				</b-overlay>
			</div>
		</div>
	</div>
</template>

<script>
	import VNav from "../components/VNav.vue";
	import Vuex from "vuex";

	const mapState = Vuex.mapState;
	const mapActions = Vuex.mapActions;
	const mapMutations = Vuex.mapMutations;

	export default {
		data() {
			return {
				sd: "",
				ed: "",
				sr: -1,
				er: -1,
			};
		},
		computed: {
			...mapState("auth", ["login_adminEmail"]),
			...mapState("form", ["loading", "legal","success", "roomList", "form", "summary"])
		},
		methods: {
			...mapActions("form", ["getForm", "getRoomList", "downloadForm"]),
			...mapMutations("form", ["set_legal"]),
			gf: function() {
				if (this.sd == "" || this.ed == "" ||
					this.sr == -1 || this.er == -1) {
					this.set_legal(false);
					return;
				}
				this.set_legal(true);
				var data = {
					sd: this.sd,
					ed: this.ed,
					sr: this.sr,
					er: this.er
				};
				this.getForm(data);
			},
			df: function(op) {
				if (this.form == [] || this.summary == []) {
					this.set_legal(false);
					return;
				}
				this.set_legal(true);
				this.downloadForm(op);
			}
		},
		components: {
			VNav
		},
		created() {
			this.getRoomList();
		}
	};
</script>
