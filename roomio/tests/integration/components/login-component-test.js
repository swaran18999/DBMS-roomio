import { module, test } from 'qunit';
import { setupRenderingTest } from 'roomio/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | login-component', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<LoginComponent />`);

    assert.dom(this.element).hasText('');

    // Template block usage:
    await render(hbs`
      <LoginComponent>
        template block text
      </LoginComponent>
    `);

    assert.dom(this.element).hasText('template block text');
  });
});
