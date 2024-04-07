import Route from '@ember/routing/route';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class SearchRoute extends Route {
	@service ajaxfw;
	@tracked searchOutput = [];
    setupController(controller) {
        controller.set('hasData', false)
        controller.set('currentRoute', this);
    }
    @action
    handleSearchInput(event) {
        this.controller.set("searchOutput", []);
        let searchInput = event.target.value
        // console.log('Search input:', searchInput);
        let self = this;
        this.ajaxfw.request("/search_unit/" + searchInput).then(
            (res) => {
                console.log(res);
                self.controller.set("searchOutput", res.data)
                self.controller.set("hasData", true)
            },
            (err) => {
                console.log('err');
                console.log(err);
            }
        );
	}
}
