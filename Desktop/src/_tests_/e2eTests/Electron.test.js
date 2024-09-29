const { _electron: electron } = require('playwright');
const path = require('path');
const { test, expect, suite } = require('@playwright/test');

test.describe('Electron App E2E Tests', () => {
  let electronApp;
  let window;

  // Before each test, launch the Electron app
  test.beforeEach(async () => {
    electronApp = await electron.launch({
      args: [path.join(__dirname, '../../electron.js')], // Update path as needed
    });
    window = await electronApp.firstWindow();
    await window.waitForLoadState('domcontentloaded'); // Ensure content is loaded
  });

  // After each test, close the Electron app
  test.afterEach(async () => {
    await electronApp.close();
  });

  test('should launch the Electron app and verify title', async () => {
    const title = await window.title();
    expect(title).toBe(''); // Ensure this matches the actual title of your app
  });

  test('should have a specific element on the page', async () => {
    const button = await window.$('button#login'); // Check for a button with id 'my-button'
    expect(button).not.toBeNull(); // Ensure the button exists
  });

  test('should change text on button click', async () => {
    const button = await window.$('button#login');
    await button.click(); // Simulate the button click

    const resultText = await window.$eval('#result', el => el.textContent); // Get the text after click
    expect(resultText).toBe('Expected Result After Click'); // Replace with the actual expected result
  });

  test('should send and receive IPC message', async () => {
    // Listen for an IPC message from the renderer
    const ipcMessage = new Promise(resolve => {
      electronApp.evaluate(({ ipcMain }) => {
        ipcMain.on('message-from-renderer', (event, arg) => {
          resolve(arg); // Resolve the promise with the message
        });
      });
    });

    // Send an IPC message from the renderer process
    await window.evaluate(() => {
      window.electron.ipcRenderer.send('message-from-renderer', 'Hello from Renderer');
    });

    // Ensure the main process received the message
    const receivedMessage = await ipcMessage;
    expect(receivedMessage).toBe('Hello from Renderer');
  });

  test('should have a functioning sidebar', async () => {
    const sidebar = await electronApp.evaluate(({ Sidebar }) => {
      return Sidebar.getApplicationSidebar();
    });

    const sidebarItem = sidebar.items.find(item => item.label === 'Pipes'); // 
    expect(sidebarItem).not.toBeNull(); // Ensure the menu item exists
  });

  test('should have correct window size and allow resizing', async () => {
    const size = await window.evaluate(() => ({
      width: window.innerWidth,
      height: window.innerHeight,
    }));
    expect(size.width).toBe(800); // Check initial window width
    expect(size.height).toBe(800); // Check initial window height

    // Maximize the window and check the new size
    await window.evaluate(() => window.maximize());
    const maximizedSize = await window.evaluate(() => ({
      width: window.innerWidth,
      height: window.innerHeight,
    }));
    expect(maximizedSize.width).toBeGreaterThan(800); // Window should be bigger after maximizing
    expect(maximizedSize.height).toBeGreaterThan(800);
  });

  test('should open and close DevTools', async () => {
    // Open DevTools
    await window.evaluate(() => {
      window.webContents.openDevTools();
    });

    const isDevToolsOpened = await window.webContents.isDevToolsOpened();
    expect(isDevToolsOpened).toBe(true); // Ensure DevTools is opened

    // Close DevTools
    await window.evaluate(() => {
      window.webContents.closeDevTools();
    });

    const isDevToolsClosed = await window.webContents.isDevToolsOpened();
    expect(isDevToolsClosed).toBe(false); // Ensure DevTools is closed
  });
});

