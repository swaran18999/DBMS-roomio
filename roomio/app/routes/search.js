import Route from '@ember/routing/route';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class SearchRoute extends Route {
  @service ajaxfw;
  @tracked searchOutput = [];
  setupController(controller) {
    controller.set('hasData', false);
    controller.set('currentRoute', this);
  }
  @action
  handleSearchInput(event) {
    this.controller.set('searchOutputUnits', []);
    this.controller.set('searchOutputBuild', []);
    this.controller.set('hasUnitData', false);
    this.controller.set('hasBuildingData', false);
    let searchInput = event.target.value;
    // console.log('Search input:', searchInput);
    let self = this;
    this.ajaxfw.request('/search_unit/' + searchInput).then(
      (res) => {
        console.log(res);
        self.controller.set('searchOutputUnits', res.data);
        self.controller.set('hasUnitData', true);
      },
      (err) => {
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.log('err');
        console.log(err);
      }
    );
    this.ajaxfw.request('/search_building/' + searchInput).then(
      (res) => {
        console.log(res);
        self.controller.set('searchOutputBuild', res.data);
        self.controller.set('hasBuildingData', true);
      },
      (err) => {
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.log('err');
        console.log(err);
      }
    );
  }
}
