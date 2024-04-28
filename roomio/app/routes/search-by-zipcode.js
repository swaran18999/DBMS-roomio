import Route from '@ember/routing/route';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';
export default class SearchByZipcodeRoute extends Route {
    @service ajaxfw;
    setupController(controller) {
        controller.set('hasData', "");
        controller.set('currentRoute', this);
    }
    @action
    search_by_zipcode() {
        this.controller.set('searchOutput', []);
        // this.controller.set('hasZipcodeData',false);
        // let zipcode = this.controller.target.zipcode;
        console.log(this.controller.zipcode);
        let self = this;

        this.ajaxfw.request('/search_by_zipcode/' + this.controller.zipcode).then(
            (res) => {
              self.controller.set('searchOutput', res.data);
              self.controller.set('hasZipcodeData', true);
              console.log(self.controller.searchOutput)
            },
            (err) => {
              console.log('Error:', err);
              if (err.status === 401) {
                this.router.transitionTo('login'); // Redirect to login if unauthorized
              }
              self.controller.set('searchOutput', []);
              self.controller.set('hasZipcodeData', false);
              console.log('error actually')
            }
          );
        }
      }



