import { module, test } from 'qunit';
import { setupTest } from 'roomio/tests/helpers';

module('Unit | Service | ajaxfw', function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test('it exists', function (assert) {
    let service = this.owner.lookup('service:ajaxfw');
    assert.ok(service);
  });
});
