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
        this.controller.set("isFav", false);
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
    this.getComments(unitID);
    this.isInterested(unitID);
  },
  setupController(controller) {
    controller.set('currentRoute', this);
    controller.set("rating", 3);
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
  getComments(unitID) {
    this.ajaxfw.request('/view_comments/' + unitID).then(
      (res) => {
        console.log(res)
        this.controller.set("ratings", res.data)
      },
      (err) => {
        this.controller.set("ratings", null)
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.error(err);
      }
    )
  },
  isInterested(unitID) {
    this.ajaxfw.request('/is_favourite/' + unitID).then(
      (res) => {
        console.log(res)
        this.controller.set("isFav", res.isFav)
      },
      (err) => {
        this.controller.set("isFav", false)
        if (err.status == 401) {
          this.router.transitionTo('login');
        }
        console.error(err);
      }
    )
  },
  actions: {
    deleteFavourite() {
      let unitID = this.controller.get("unitID");
      this.ajaxfw.request('/remove_as_favourite/' + unitID).then(
        (res) => {
          console.log(res)
          this.isInterested(unitID);
        },
        (err) => {
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.log(err);
        }
      );
    },
    markAsFavourite() {
      let unitID = this.controller.get("unitID");
      console.log(unitID)
      let data = {
        "UnitRentID": unitID, 
      }
      this.ajaxfw.post('/add_as_favourite', { data: data }).then(
        (res) => {
          console.log(res)
          this.isInterested(unitID);
        },
        (err) => {
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.log(err);
        }
      );
    },
    confirmRatingDelete(rating) {
      let unitID = this.controller.get("unitID");
      this.ajaxfw
      .request('/delete_comment', {
        method: 'POST',
        data: {
          "CommentID": rating.CommentID
        },
      })
      .then(
        (res) => {
          console.log(res);
          this.getComments(unitID);
        },
        (err) => {
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.error(err);
        }
      );
    },
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
    deleteRating(rating) {
      set(rating, "is_delete", true)
    },
    cancelRatingDelete(rating) {
      set(rating, "is_delete", false)
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
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.log(err);
        }
      );
    },
    confirmRating(stars) {
      this.controller.set("rating", stars)
    },
    addRating() {
      let unitID = this.controller.get("unitID");
      let rating = this.controller.get("rating");
      let commentText = this.controller.get("commentText");
      console.log(unitID, rating, commentText);
      
      let data = {
        "UnitRentID": unitID,
        "Rating": rating,
        "Comment": commentText
      };
      console.log(data)
      this.ajaxfw.post('/add_comment', { data: data }).then(
        (res) => {
          console.log(res);
          this.getComments(unitID);
        },
        (err) => {
          if (err.status == 401) {
            this.router.transitionTo('login');
          }
          console.log(err);
        }
      );
    },
  }
});
