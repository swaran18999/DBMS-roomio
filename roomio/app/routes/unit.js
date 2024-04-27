import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';
import { set } from '@ember/object';

export default Route.extend({
  ajaxfw: service(),
  router: service(),
  beforeModel(params) {
    console.log(params.to.params['unitID']);
    let unitID = params.to.params['unitID'];
    this.ajaxfw.request('/search_unit/' + unitID).then(
      (res) => {
        let data = res.data;
        this.controller.set(
          'AvailableDateForMoveIn',
          data.AvailableDateForMoveIn
        );
        this.controller.set("unitID", unitID);
        this.controller.set('MonthlyRent', data.MonthlyRent);
        this.controller.set('UnitNumber', data.UnitNumber);
        this.controller.set('squareFootage', data.squareFootage);
      },
      (err) => {
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.error(err);
      }
    );
    this.getInterests(unitID);
  },
  setupController(controller) {
    controller.set('currentRoute', this);
  },
  getInterests(unitID) {
    this.ajaxfw.request('/view_interests/' + unitID).then(
      (res) => {
        console.log(res)
        this.controller.set("interests", res.data)
      },
      (err) => {
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.error(err);
      }
    )
  },
  actions: {
    confirmDelete(interest) {
      let unitID = this.controller.get("unitID");
      this.ajaxfw
      .request('/delete_interest', {
        method: 'POST',
        data: interest,
      })
      .then(
        (res) => {
          console.log(res);
          this.getInterests(unitID);
        },
        (err) => {
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.error(err);
        }
      );
    },
    cancelDelete(unit) {
      set(unit, "is_delete", false)
    },
    deleteInterest(unit) {
      set(unit, "is_delete", true)
    },
    markAsInterested() {
      let unitID = this.controller.get("unitID");
      let moveInDate = this.controller.get("moveInDate");
      let roommatesCount = this.controller.get("roommatesCount");
      console.log(unitID, moveInDate, roommatesCount)
      let data = {
        "UnitRentID": unitID, 
        "MoveInDate": moveInDate, 
        "RoommateCnt": roommatesCount
      }
      this.ajaxfw.post('/add_interest', { data: data }).then(
        (res) => {
          console.log(res)
          this.getInterests(unitID);
        },
        (err) => {
          console.log(err);
        }
      );
    }
  }
});
