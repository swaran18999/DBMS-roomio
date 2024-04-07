import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default Route.extend({
  // ajax: service('ajax-fw'),
  ajaxfw: service(),
  setupController(controller) {
    controller.set('currentRoute', this);
  },
  actions: {
    abc() {
      console.log('abc clicked');
      this.ajaxfw.request('/trial').then(res=>{
        console.log(res)
      }, err=>{
        console.log("err");
        console.log(err)
      });
    },
  },
});
