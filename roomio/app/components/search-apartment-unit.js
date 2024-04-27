// app/components/search-apartment-unit.js
import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
  ajaxfw: service(),
  router: service(),
  buildingName: 'Mary Island',
  companyName: 'Ramos Inc',

  actions: {
    goToUnit(UnitRentID) {
      this.router.transitionTo('unit', UnitRentID);
    },
    searchApartments() {
      this.set('searchOutputUnits', null);
      let data = {
        companyName: this.companyName,
        buildingName: this.buildingName,
      };
      this.ajaxfw
        .post('/search_apartment', {
          data: data,
        })
        .then(
          (res) => {
            this.set('searchOutputUnits', res.data);
            console.log(res);
          },
          (err) => {
            console.error(err);
          }
        );
    },
  },
});
