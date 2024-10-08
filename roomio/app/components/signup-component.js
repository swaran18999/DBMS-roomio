// app/components/pet-details.js
import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
  router: service(),
  ajaxfw: service(),
  newUsername: null,
  newFirstName: null,
  newLastName: null,
  newDOB: null,
  newGender: null,
  newEmail: null,
  newPhone: null,
  newPassword: null,
  confirmPassword: null,
  signupSuccess: false,
  signupError: null,
  init() {
    this._super(...arguments);
    this.set('newGender', '0');
    let currentDate = new Date();
    currentDate = currentDate.toISOString().substring(0, 10);
    this.set("today", currentDate)
  },
  actions: {
    genderClicked(event) {
      this.set('newGender', event.target.value);
    },
    goToLogin() {
      this.router.transitionTo('login');
    },
    async signup(event) {
      let {
        newUsername,
        newFirstName,
        newLastName,
        newDOB,
        newGender,
        newEmail,
        newPhone,
        newPassword,
        confirmPassword,
      } = this;
      let data = {
        newUsername: newUsername,
        newFirstName: newFirstName,
        newLastName: newLastName,
        newDOB: newDOB,
        newGender: newGender,
        newEmail: newEmail,
        newPhone: newPhone,
        newPassword: newPassword,
        confirmPassword: confirmPassword,
      };
      console.log(data);
      if (newPassword != confirmPassword) {
        this.set('signupError', 'Passwords do not match!');
      } else {
        try {
          this.ajaxfw.post('/signup', { data: data }).then(
            (res) => {
              this.set('signupSuccess', true);
            },
            (err) => {
              if(err.status == 409) {
                this.set(
                  'signupError',
                  'This username already exist!'
                );
              }
              console.log(err);
            }
          );
        } catch (error) {
          this.set('signupError', error.message);
          if(error.status == 409) {
            this.set(
              'signupError',
              'This username already exist!'
            );
          }
        }
      }
    },
  },
});
