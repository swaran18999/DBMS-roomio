import { module, test } from 'qunit';
import { setupTest } from 'roomio/tests/helpers';

module('Unit | Route | building', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    let route = this.owner.lookup('route:building');
    assert.ok(route);
  });
});
