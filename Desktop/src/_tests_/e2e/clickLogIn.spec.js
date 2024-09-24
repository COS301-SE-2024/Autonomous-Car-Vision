const { test, expect, _electron: electron } = require('@playwright/test');

test('click the Log In button', async () => {
  // Launch Electron app
  const electronApp = await electron.launch({ args: ['.'] });

  // Wait for the first BrowserWindow to open and get the Page object
  const window = await electronApp.firstWindow();

  // Set window size
  await window.setViewportSize({ width: 800, height: 800 });

  // Wait for the page to load fully
  await window.waitForLoadState('domcontentloaded');

  // Click the button with text "Log In"
  await window.click('text=Log In');

  // Take a screenshot
  await window.screenshot({ path: 'clickedLogin.png' });

  // Close the app
  await electronApp.close();
});
