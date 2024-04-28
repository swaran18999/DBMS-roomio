// app/components/pet-details.js
import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
  ajaxfw: service(),
  router: service(),
  petName: '',
  petType: 'Dog',
  petSize: 'Small',

  actions: {
    petTypeChanged(event) {
      this.set('petType', event.target.value);
    },
    petSizeChanged(event) {
      this.set('petSize', event.target.value);
    },
    savePetDetails() {
      let data = {
        pet_name: this.petName,
        pet_type: this.petType,
        pet_size: this.petSize,
      };
      this.ajaxfw
        .post('/register_pet', {
          data: data,
        })
        .then(
          (res) => {
            console.log(res);
            console.log('Saved successfully');
            this.router.transitionTo("user.pets");
          },
          (err) => {
            console.log(err.statusCode);
            if(err.status == 409) {
              this.set(
                'errorMessage',
                'This pet already exist!'
              );
            }
            console.error(err);
          }
        );
    },
  },
});
