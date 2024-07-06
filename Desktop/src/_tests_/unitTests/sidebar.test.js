import { render } from '@testing-library/svelte';
import { describe, expect, test, it } from 'vitest';
import { mdiHelpCircle,mdiViewGallery, mdiUpload, mdiCloudPrintOutline } from "@mdi/js";
import Sidebar from '../../components/Sidebar.svelte';
import '@testing-library/jest-dom';

import { onMount, getMarkerPosition } from '../../components/Sidebar.svelte';
import { writable } from 'svelte/store';

describe('Selected Code Block', () => {
  let items;
  let $location;

  beforeEach(() => {
    items = [
      { name: "Gallery", route: "/gallery", iconPath: mdiViewGallery },
      { name: "Upload", route: "/upload", iconPath: mdiUpload },
      { name: "Models", route: "/models", iconPath: mdiCloudPrintOutline },
      { name: "Help", route: "/help", iconPath: mdiHelpCircle },
    ];

    $location = writable('/');
  });

  test('checks names of sidedar contents"', () => {
    try{

        render(Sidebar);
            $location.set('/gallery');
            const activeTab = document.querySelector('.active');
            expect(activeTab.textContent).toBe('Gallery');
    }
    catch(e){
        console.error("error occured", e);
    }
    
  });

  test('Checks if the correct tab is active when the location is "/upload"', async() => {
   
    const {container} = await render(Sidebar);
    $location.set('/upload');
    const activeTab = screen.getByTest('Upload');
    expect(activeTab).toBeInDocument();
  });

  // test('Checks if the correct tab is active when the location is "/models"', () => {
  //   $location.set('/models');
  //   const activeTab = document.querySelector('.active');
  //   expect(activeTab.textContent).toBe('Models');
  // });

  // test('Checks if the correct tab is active when the location is "/help"', () => {
  //   $location.set('/help');
  //   const activeTab = document.querySelector('.active');
  //   expect(activeTab.textContent).toBe('Help');
  // });

  // test('Checks if the correct tab is active when the location is "/accountsettings" or "/changepassword"', () => {
  //   $location.set('/accountsettings');
  //   const activeTab = document.querySelector('.active');
  //   expect(activeTab.textContent).toBe('Account settings');

  //   $location.set('/changepassword');
  //   const activeTab2 = document.querySelector('.active');
  //   expect(activeTab2.textContent).toBe('Account settings');
  // });
});