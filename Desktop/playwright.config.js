const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './src/_tests_/e2eTests/',

  timeout: 30 * 1000,

  use: {
    headless: true, 
  },

  retries: 0,

  fullyParallel: true,

  reporter: 'html', 

  projects: [
    {
      name: 'Electron',
      use: { browserName: 'webkit' },
    },
  ],
});