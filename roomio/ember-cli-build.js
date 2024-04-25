'use strict';

const EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    svgJar: {
      sourceDirs: [
        'public/icons',
      ],
    },
    // Add options here
  });

  return app.toTree();
};
