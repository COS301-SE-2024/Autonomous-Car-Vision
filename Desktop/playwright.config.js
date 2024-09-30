// playwright.config.js
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  // Directory where your test files are located
  testDir: './src/_tests_/e2eTests/',

  // Global test timeout (in milliseconds)
  timeout: 30 * 1000,

  // Option to run in headless mode or with GUI
  use: {
    headless: true, // Set to false if you want to see the browser window
  },

  // Maximum number of retries if a test fails
  retries: 0,

  // Run tests in parallel
  fullyParallel: true,

  // Reporter settings
  reporter: 'html', // Use 'html' or 'json' for more detailed reports

  // Browsers configuration
  projects: [
    {
      name: 'Electron',
      use: { browserName: 'webkit' },
    },
  ],
});