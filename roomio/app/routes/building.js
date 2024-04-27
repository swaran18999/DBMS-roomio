import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default Route.extend({
  ajaxfw: service(),
  router: service(),
  beforeModel(params) {
    console.log(params.to.params['company']);
    let company = params.to.params['company'];
    let building = params.to.params['building'];
    console.log(company, building)
    // this.ajaxfw.request('/search_unit/' + unitID).then(
    //   (res) => {
    //     let data = res.data;
    //     this.controller.set(
    //       'AvailableDateForMoveIn',
    //       data.AvailableDateForMoveIn
    //     );
    //     this.controller.set('MonthlyRent', data.MonthlyRent);
    //     this.controller.set('UnitNumber', data.UnitNumber);
    //     this.controller.set('squareFootage', data.squareFootage);
    //   },
    //   (err) => {
    //     if (err.status == 401) {
    //       this.router.transitionTo('login');
    //     }
    //     console.error(err);
    //   }
    // );
  },
});
