const api = 'http://127.0.0.1:5000/form/';

const axios = require("axios");
const json2csvParser = require("json2csv").Parser

export default {
	state: {
		loading: false,
		roomList: [],
		form: [],
		summary: [],
		legal: false,
		success:false
	},
	mutations: {
		flip_loading(state) {
			state.loading = !state.loading;
		},
		set_loading(state, val) {
			state.loading = val;
		},
		set_form(state, form) {
			state.form = form;
		},
		set_roomList(state, n) {
			state.roomList = n;
		},
		set_summary(state, s) {
			state.summary = s;
		},
		set_legal(state, b) {
			state.legal = b;
		},
		flip_legal(state) {
			state.legal = !state.legal;
		},
		set_success(state,v){
			state.success=v;
		},
		nop() {
			return;
		}
	},
	actions: {
		getForm({
			commit
		}, data) {
			commit("set_loading", true);
			return axios.post(api + 'rep', data)
				.then(function(res) {
					commit('set_loading', false);
					var summary = [];
					var t = res.data;
					var explain = ["Turn on Or Turn Off", "Set temperature",
						"Set speed", "Regular update" , "Blowing State Changed"
					];
					for (var i = 0; i < t.length; i++) {
						var flag = false;
						for (var j = 0; j < summary.length; j++) {
							if (summary[j].id == t[i].id) {
								summary[j].On_Off_Times += (t[i].type == 1 ? 1 : 0);
								summary[j].cost += t[i].wind * 5;
								flag = true;
								break;
							}
						}
						if (flag == false)
							summary.push({
								id: t[i].id,
								On_Off_Times: (t[i].type == 1 ? 1 : 0),
								cost: t[i].wind * 5
							});
						t[i].type = explain[t[i].type - 1];
					}
					commit("set_success",true);
					commit('set_form', t);
					commit('set_summary', summary);
				})
				.catch((error) => {
					console.log(error)
				});
		},
		getRoomList({
			commit
		}) {
			return axios.get(api + 'roomList')
				.then(
					function(rl) {
						commit('set_roomList', rl.data);
					}
				)
				.catch((error) => {
					console.log(error)
				});
		},
		downloadForm({
			commit,state
		},op) {
			commit("nop")
			var x,target,fields;
			if (op==true) {
				target=state.summary;
				x="summary";
				fields=["id","On_Off_Times","cost"];
			}else{
				target=state.form;
				x="details";
				fields=["id","time","type","old","new","wind","cost"];
			}
			if(target==[]) return;
			var opt={fields:fields};
			const parser = new json2csvParser();
			//target=JSON.stringify(target);
			const csv = parser.parse(target,opt);
			console.log(csv);
			const blob = new Blob(
				['\uFEFF' + csv], {
					type: 'text/plain;charset=utf-8;'
				}
			);

			let url = window.URL.createObjectURL(blob);
			let link = document.createElement("a");
			link.style.display = "none";
			link.href = url;
			link.download = x + ".csv"
			document.body.appendChild(link);
			link.click();
		}
	},
	namespaced: true
}
