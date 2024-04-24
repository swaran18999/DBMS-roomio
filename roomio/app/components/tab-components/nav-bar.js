import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
  router: service(),
	ajaxfw: service(),
	actions: {
    logout() {
      try {
				this.ajaxfw.post('/logout').then(
					(res) => {
            if(res.flag == 1) {
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
	},
});
