import { module, test } from 'qunit';
import { setupTest } from 'roomio/tests/helpers';

module('Unit | Route | search-by-zipcode', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    let route = this.owner.lookup('route:search-by-zipcode');
    assert.ok(route);
  });
});
