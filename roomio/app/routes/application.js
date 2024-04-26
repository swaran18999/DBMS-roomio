import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default Route.extend({
  ajaxfw: service(),
  router: service(),
  afterModel() {
    this._super(...arguments);
    if (this._router.url == '/') {
      this.router.transitionTo('login');
    }
  },
});
