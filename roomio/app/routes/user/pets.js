import Route from '@ember/routing/route';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class UserPetsRoute extends Route {
  @service ajaxfw;
  setupController(controller) {
    controller.set('currentRoute', this);
  }
  @action
  savePetDetailsAPI(data) {
    console.log('savePetDetailsAPI');
    console.log(data);
    this.ajaxfw
      .post('/register_pet', {
        data: data,
      })
      .then(
        (res) => {
          console.log(res);
          console.log('Saved successfully');
        },
        (err) => {
          console.log('err');
          console.log(err);
        }
      );
  }
}
