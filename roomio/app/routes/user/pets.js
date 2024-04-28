import Route from '@ember/routing/route';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';
import { set } from '@ember/object';

export default class UserPetsRoute extends Route {
  @service router;
  @service ajaxfw;
  model() {
    super.model(...arguments);
    this.fetchPets();
  }
  fetchPets() {
    this.ajaxfw.request('/get_pet').then(
      (res) => {
        let pets = res['pets'];
        pets.forEach((pet) => {
          pet['is_editable'] = false;
          pet['is_delete'] = false;
          pet['old_pet_name'] = pet['pet_name'];
          pet['old_pet_type'] = pet['pet_type'];
        });
        this.controller.set('petsList', pets);
        console.log(res);
      },
      (err) => {
        console.error(err);
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
      }
    );
  }
  setupController(controller) {
    controller.set('currentRoute', this);
  }
  @action addPets() {
    this.router.transitionTo('user.addPets');
  }
  @action editPets(pet) {
    set(pet, 'is_editable', true);
  }
  @action deletePets(pet) {
    set(pet, 'is_delete', true);
  }
  @action confirmDeletePets(pet) {
    this.ajaxfw
      .request('/delete_pet', {
        method: 'POST',
        data: pet,
      })
      .then(
        (res) => {
          console.log(res);
          this.fetchPets();
        },
        (err) => {
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.error(err);
        }
      );
  }
  @action petTypeChanged(pet, e) {
    set(pet, 'pet_type', e.target.value);
  }
  @action petSizeChanged(pet, e) {
    set(pet, 'pet_size', e.target.value);
  }
  @action savePets(pet, e) {
    this.ajaxfw
      .request('/update_pet', {
        method: 'POST',
        data: pet,
      })
      .then(
        (res) => {
          console.log(res);
          this.fetchPets();
        },
        (err) => {
          if (err.status == 409) {
            set(pet, "is_duplicate", true);
          }
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.error(err);
        }
      );
  }
  @action cancelEdit(pet, e) {
    this.fetchPets();
  }
}
