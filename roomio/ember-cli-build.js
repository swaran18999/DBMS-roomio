'use strict';

const EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    svgJar: {
      sourceDirs: [
        'node_modules/material-design-icons/file/svg/design',
        'node_modules/material-design-icons/action/svg/design',
        'public/icons',
      ],
    },
    // Add options here
  });

  return app.toTree();
};
