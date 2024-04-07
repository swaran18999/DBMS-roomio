import { module, test } from 'qunit';
import { setupTest } from 'roomio/tests/helpers';

module('Unit | Route | user/pets', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    let route = this.owner.lookup('route:user/pets');
    assert.ok(route);
  });
});
