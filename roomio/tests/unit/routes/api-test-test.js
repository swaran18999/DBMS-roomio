import { module, test } from 'qunit';
import { setupTest } from 'roomio/tests/helpers';

module('Unit | Route | api-test', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    let route = this.owner.lookup('route:api-test');
    assert.ok(route);
  });
});
