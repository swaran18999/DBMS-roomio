import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default Route.extend({
  ajaxfw: service(),
  router: service(),
  beforeModel() {
    this.ajaxfw.request('/get_user_details').then(
      (res) => {
        console.log(res);
        let data = res.data;
        this.controller.set('UserName',data.UserName);
        this.controller.set('FirstName', data.FirstName);
        this.controller.set('LastName', data.LastName);
        this.controller.set('DOB', data.DOB);
        this.controller.set('Gender', data.Gender);
        this.controller.set('Email', data.Email);
        this.controller.set('Phone', data.Phone);
      },
      (err) => {
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.error(err);
      }
    );
	this.ajaxfw.request('/get_user_favourites').then(
		(res) => {
			console.log(res);
			this.controller.set("favourites", res.data)
		},
		(err) => {
			if (err.status == 401) {
				this.router.transitionTo('login');
			}
			console.error(err);
		}
    );  
  },
});
