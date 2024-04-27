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
    this.ajaxfw.post('/search_building', {
      data: {
        "companyName": company,
        "buildingName": building
      }
    }).then(
      (res) => {
        let data = res.data;
        this.controller.set('CompanyName', data.CompanyName);
        this.controller.set('BuildingName', data.BuildingName);
        this.controller.set('Address', data.Address);
        this.controller.set('amenitieslist',data.amenitieslist);
        this.controller.set('YearBuilt',data.YearBuilt);
        this.controller.set('NumUnitsAvailableForRent',data.NumUnitsAvailableForRent);
      },
      (err) => {
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.error(err);
      }
    );
  },
});
