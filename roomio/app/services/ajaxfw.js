import FetchService from 'ember-ajax-fetch/services/fetch';

export default class ExtendedFetchService extends FetchService {
  get headers() {
    let headers = {};
    headers['Access-Control-Allow-Origin'] = '*';
    headers['Content-Type'] = 'application/json';
    return headers;
  }
}
