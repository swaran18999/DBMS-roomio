import Route from '@ember/routing/route';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class UserPetsRoute extends Route {
  @service router;
  @service ajaxfw;
  model() {
    super.model(...arguments);
    this.ajaxfw.request('/get_pet').then(
      (res) => {
        this.controller.set('petsList', res['pets']);
        console.log(res);
      },
      (err) => {
        console.error(err);
      }
    );
  }
  setupController(controller) {
    controller.set('currentRoute', this);
  }
  @action
  addPets() {
    this.router.transitionTo('user.addPets');
  }
}
