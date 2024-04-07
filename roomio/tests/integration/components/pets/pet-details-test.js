import { module, test } from 'qunit';
import { setupRenderingTest } from 'roomio/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | pets/pet-details', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Pets::PetDetails />`);

    assert.dom(this.element).hasText('');

    // Template block usage:
    await render(hbs`
      <Pets::PetDetails>
        template block text
      </Pets::PetDetails>
    `);

    assert.dom(this.element).hasText('template block text');
  });
});
