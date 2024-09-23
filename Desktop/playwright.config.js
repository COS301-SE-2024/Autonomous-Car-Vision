// playwright.config.js
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './src/_tests_/e2e', // Set your e2e test directory here
  // You can add more configuration options if needed
  projects: [
    {
      name: 'electron',
      use: {
        channel: 'chrome', // Ensures Electron tests run correctly
      },
    },
  ],
});
