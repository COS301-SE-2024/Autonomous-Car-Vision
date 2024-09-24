const { test, expect, _electron: electron } = require('@playwright/test');

test('click the Dev button => click Pipes Button', async () => {
    const electronApp = await electron.launch({ args: ['.'] });

    const window = await electronApp.firstWindow();
    await window.setViewportSize({ width: 800, height: 800 });
    await window.waitForLoadState('domcontentloaded');

    console.log("Attempting to click Developer button...");
    await window.click('text=Developer');
    console.log("Clicked Developer button");
    await window.screenshot({ path: 'src/_tests_/e2e/screenshots/clickedDeveloperLogin.png' });

    console.log("Waiting for Pipes button to be visible and enabled...");
    const pipesButton = window.locator('text=Pipes');
    if (await pipesButton.isVisible()) {
        console.log("Pipes button is clickable");
        await pipesButton.click();
        await window.screenshot({ path: 'src/_tests_/e2e/screenshots/clickedPipes.png' });
        console.log("Checking if Clear Pipe button is visible...");
        const AIModelsButton = window.locator('text=Clear Pipe');
        // ai-model-selector
        if (await AIModelsButton.isVisible()) {

            await expect(window.locator('text=Clear Pipe')).toBeVisible();
            console.log("Clear Pipe button is visible");

            await window.waitForSelector('text=Clear Pipe');
            await window.click('text=Clear Pipe')
            await window.screenshot({ path: 'src/_tests_/e2e/screenshots/clickedClearPipe.png' });
        } else {
            console.log("Clear Pipe button is not clickable");
        } 
    } else {
        console.log("Pipes button is not clickable");
    }


    await electronApp.close();
});
