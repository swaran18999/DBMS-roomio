import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default Route.extend({
	ajaxfw: service(),
	router: service(),
	beforeModel() {
		this._super(...arguments);
		try {
			this.ajaxfw.request('/').then(
				(res) => {
					if(res.flag == 1) {
						this.router.transitionTo("home");
					}
					else if(res.flag == 2) {
						this.router.transitionTo("login");
					}
					else {
						console.error(res);
					}
				},
				(err) => {
					console.error(err);
				}
			);
		} catch (error) {
			console.error(error);
		}
	}
});
