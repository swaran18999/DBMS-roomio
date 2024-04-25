// app/components/pet-details.js
import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
	ajaxfw: service(),
	router: service(),
	apiName: '',
	method: 'POST',
	data: '',
	actions: {
		methodChanged(event) {
			this.set('method', event.target.value);
		},
		sendAPI() {
			this.ajaxfw
				.request(this.apiName, {
					data: this.data.trim() == "" ? "" : JSON.parse(this.data),
					method: this.method
				})
				.then(
					(res) => {
						console.log(res);
					},
					(err) => {
						console.error(err);
					}
				);
		},
	},
});
