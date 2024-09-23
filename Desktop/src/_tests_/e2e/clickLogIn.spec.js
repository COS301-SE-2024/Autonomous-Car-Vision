const { test, expect, _electron: electron } = require('@playwright/test');

test('click the Log In button', async () => {
  // Launch Electron app
  const electronApp = await electron.launch({ args: ['.'] });

  // Wait for the first BrowserWindow to open and get the Page object
  const window = await electronApp.firstWindow();

  // Set window size
  await window.setViewportSize({ width: 800, height: 600 });

  // Wait for the page to load fully
  await window.waitForLoadState('domcontentloaded');

  // Click the button with text "Log In"
  await window.click('text=Log In');

  // Take a screenshot
  await window.screenshot({ path: 'clickedLogin.png' });

  // Optionally, check if a certain element exists after clicking
  // For example, check if the URL or another element changes after clicking
  // await expect(window).toHaveURL('expected-url');  // Adjust this according to the app behavior
  // OR check for an element appearing after login
  // await expect(window.locator('text=Welcome')).toBeVisible();  // Adjust the selector

  // Close the app
  await electronApp.close();
});
