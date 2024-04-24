import { module, test } from 'qunit';
import { setupRenderingTest } from 'roomio/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | signup-component', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<SignupComponent />`);

    assert.dom(this.element).hasText('');

    // Template block usage:
    await render(hbs`
      <SignupComponent>
        template block text
      </SignupComponent>
    `);

    assert.dom(this.element).hasText('template block text');
  });
});
