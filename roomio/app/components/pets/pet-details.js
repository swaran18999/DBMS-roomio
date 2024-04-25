// app/components/pet-details.js
import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
  ajaxfw: service(),
	router: service(),
  petName: '',
  petType: '',
  petSize: '',
  username: '',

  actions: {
		petTypeChanged(event) {
			this.set("petType", event.target.value)
		},
		petSizeChanged(event) {
			this.set("petSize", event.target.value)
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
          },
          (err) => {
            console.error(err);
          }
        );
    },
  },
});
