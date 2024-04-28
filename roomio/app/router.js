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
  });
  this.route('user_details');
  this.route('unit', { path: '/unit/:unitID' });
  this.route('search');
  this.route('login');
  this.route('signup');
  this.route('api-test');
  this.route('building', { path: '/building/:company/:building' });
  this.route('search-by-zipcode');
});
