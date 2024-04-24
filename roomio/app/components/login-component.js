// app/components/pet-details.js
import Component from '@ember/component';
import { service } from '@ember/service';

export default Component.extend({
  router: service(),
  ajaxfw: service(),
  username: null,
  password: null,
  actions: {
    createAccount() {
      this.router.transitionTo('signup');
    },
    async login(event) {
      let { username, password } = this;

      try {
        this.ajaxfw.post('/login', { data: { username, password } }).then(
          (res) => {
            console.log(res);
            if (res.flag == 1) {
              this.router.transitionTo('home');
            } else {
              this.set(
                'errorMessage',
                'This username and password does not exist!'
              );
            }
          },
          (err) => {
            console.log(err);
          }
        );
      } catch (error) {
        this.set('errorMessage', error.message);
      }
    },
  },
});
