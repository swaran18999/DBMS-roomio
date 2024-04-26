import FetchService from 'ember-ajax-fetch/services/fetch';

export default class ExtendedFetchService extends FetchService {
  host = 'http://localhost:8989';
  get headers() {
    let headers = {};
    headers['Access-Control-Allow-Origin'] = '*';
    headers['Content-Type'] = 'application/json';
    return headers;
  }
}
