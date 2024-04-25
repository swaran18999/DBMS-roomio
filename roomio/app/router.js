import EmberRouter from '@ember/routing/router';
import config from 'roomio/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('home');
  this.route('about');
  this.route('user', function () {
    this.route('pets');
    this.route('addPets');
    this.route('edit-pets');
  });
  this.route('search');
  this.route('login');
  this.route('signup');
  this.route('api-test');
});
