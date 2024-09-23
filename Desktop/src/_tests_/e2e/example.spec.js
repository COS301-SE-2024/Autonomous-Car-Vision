const { test, expect, _electron: electron } = require('@playwright/test');

test('example test', async () => {
  // Launch Electron app
  const electronApp = await electron.launch({ args: ['.'] });

  // Check if the app is packaged
  const isPackaged = await electronApp.evaluate(async ({ app }) => {
    return app.isPackaged;
  });
  expect(isPackaged).toBe(false);

  // Wait for the first BrowserWindow to open and get the Page object
  const window = await electronApp.firstWindow();

  // Set window size explicitly to avoid zero width issue
  await window.setViewportSize({ width: 800, height: 600 });

  // Wait for the page to load fully
  await window.waitForLoadState('domcontentloaded');

  // Take a screenshot
  await window.screenshot({ path: 'intro.png' });

  // Close the app
  await electronApp.close();
});
