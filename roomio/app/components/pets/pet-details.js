// app/components/pet-details.js
import Component from '@ember/component';

export default Component.extend({
  petName: '',
  petType: '',
  petSize: '',
  username: '',

  actions: {
    savePetDetails() {
      let data = {
        'pet_name': this.petName,
        'pet_type': this.petType,
        'pet_size': this.petSize,
        'username': "user1"
       }
      this.savePetDetailsAPI(data);
    }
  }
});
