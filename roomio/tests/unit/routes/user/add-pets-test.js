import { module, test } from 'qunit';
import { setupTest } from 'roomio/tests/helpers';

module('Unit | Route | user/addPets', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    let route = this.owner.lookup('route:user/add-pets');
    assert.ok(route);
  });
});
