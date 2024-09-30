<script>
    import Shepherd from 'shepherd.js';
    import {theme} from '../stores/themeStore';
    import { push, location } from "svelte-spa-router"; // Assuming you're using svelte-routing for navigation
    import { Icon, Button } from "svelte-materialify";
  

    let tour; // Declare tour in the top-level scope

   // Function to initialize a basic tour
  function initTour(steps) {
    tour = new Shepherd.Tour({
      defaultStepOptions: {
        scrollTo: true,
        cancelIcon: {
          enabled: true
        },
        classes: 'shepherd-theme-default shepherd-button',
      }
    });

    steps.forEach(step => {
      tour.addStep(step);
    });

    tour.start();
  }

  // Tour: Gallery
  function tourViewGallery() {
    const steps = [
      {
        id: 'go-to-gallery',
        text: 'Click here to go to the gallery page.',
        attachTo: { element: 'go-to-gallery', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/gallery');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'gallery-page',
        text: 'This is the main overview of your gallery page.',
        attachTo: { element: 'gallery-page', on: 'top' },
        buttons: [
          {
            text: 'Next',
            action: () => tour.next()
          }
        ]
      },
      {
        id: 'gallery-card',
        text: 'Click on a card to download or view it.',
        attachTo: { element: 'gallery-card', on: 'bottom' },
        buttons: [
          {
            text: 'Next',
            action: () => tour.next()
          }
        ]
      },
      {
        id: 'upload-video',
        text: 'Click on a card to upload a video.',
        attachTo: { element: 'upload-video', on: 'top' },
        buttons: [
          {
            text: 'Done',
            action: () => tour.complete()
          }
        ]
      },
    ];
          initTour(steps);  // Start the tour once the element exists
  }


  // Tour: Account Settings
  function tourAccount() {
    const steps = [
      {
        id: 'go-to-account-settings',
        text: 'Click here to go to the account settings page.',
        attachTo: { element: 'go-to-account-settings', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/accountsettings');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'account-page',
        text: 'This is the where you can change your details.',
        attachTo: { element: 'account-page', on: 'top' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/changepassword');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'password-page',
        text: 'This is where you can change your password.',
        attachTo: { element: 'password-page', on: 'top' },
        buttons: [
          {
            text: 'Done',
            action: () => tour.complete()
          }
        ]
      }
    ];
    initTour(steps);
  }

  // Tour: Models
  function tourModels() {
    const steps = [
      {
        id: 'go-to-models',
        text: 'Click here to go to the models page.',
        attachTo: { element: 'go-to-models', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/models');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'models-page',
        text: 'This is the where you can view all the different models.',
        attachTo: { element: 'models-page', on: 'top' },
        buttons: [
          {
            text: 'Next',
            action: tour.next()
          }
        ]
      },
      {
        id: 'modelsContent',
        text: 'Click on a model to view more details.',
        attachTo: { element: 'modelsCard', on: 'top' },
        buttons: [
          {
            text: 'Done',
            action: () => tour.complete()
          }
        ]
      }
    ];
    initTour(steps);
  }


   // Tour: Pipes
   function tourPipes() {
    const steps = [
      {
        id: 'go-to-pipes',
        text: 'Click here to go to the pipes page.',
        attachTo: { element: 'go-to-pipes', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/svelvet');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'pipes-page',
        text: 'This is the where you can create your own pipes using our models.',
        attachTo: { element: 'pipes-page', on: 'top' },
        buttons: [
          {
            text: 'Done',
            action: tour.complete()
          }
        ]
      }
    ];
    initTour(steps);
  }

   // Tour: Drive Gallery
   function tourDriveGallery() {
    const steps = [
      {
        id: 'go-to-drive-gallery',
        text: 'Click here to go access your drive gallery directory.',
        attachTo: { element: 'go-to-drive-gallery', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/drivegallery');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'drive-gallery-page',
        text: 'This is the main overview of your drive gallery directory.',
        attachTo: { element: 'drive-gallery-page', on: 'top' },
        buttons: [
          {
            text: 'Next',
            action: () => tour.next()
          }
        ]
      },
      {
        id: 'drive-gallery-card',
        text: 'Click on a card to view the dashboard.',
        attachTo: { element: 'drive-gallery-card', on: 'bottom' },
        buttons: [
          {
            text: 'Done',
            action: () => tour.complete()
          }
        ]
      },
    ];
          initTour(steps);  // Start the tour once the element exists
  }

   // Tour: Teams
   function tourTeams() {
    const steps = [
      {
        id: 'go-to-teams-view',
        text: 'Click here view your team members.',
        attachTo: { element: 'go-to-teams-view', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/teamView');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'team-view',
        text: 'This is where you can view and edit your team member details',
        attachTo: { element: 'team-view', on: 'top' },
        buttons: [
          {
            text: 'Next',
            action: () => tour.next()
          }
        ]
      },
      {
        id: 'team-network',
        text: 'This is the team network page. It allows you to view your team setup',
        attachTo: { element: 'team-network', on: 'top' },
        buttons: [
          {
            text: 'Done',
            action: () => {
              push('/teamNetwork');  // Navigating using svelte-spa-router
              tour.complete();
            }
          }
        ]
      },
    ];
          initTour(steps);  // Start the tour once the element exists
  }

    // Tour: Visualizer
    function tourVisualizer() {
    const steps = [
      {
        id: 'go-to-visualizer',
        text: 'Click here to go access the Netron visualizer.',
        attachTo: { element: 'go-to-visualzier', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/visualize');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'visualizer-page',
        text: 'Wait for the featured application to load.',
        attachTo: { element: 'visualzer-page', on: 'top' },
        buttons: [
          {
            text: 'Next',
            action: () => tour.next()
          }
        ]
      },
      {
        id: 'visualzier-page',
        text: 'Visit the site: netron.app for further details',
        attachTo: { element: 'visualizer-page', on: 'top' },
        buttons: [
          {
            text: 'Done',
            action: () => tour.complete()
          }
        ]
      },
    ];
          initTour(steps);  // Start the tour once the element exists
  }

</script>

{#if $theme === 'highVizLight'}
<div class="bg-highVizLight grid grid-cols-2 h-full w-full gap-3 py-2 ">
  <Button on:click={tourViewGallery}>Tour: Gallery</Button>
  <Button on:click={tourAccount}>Tour: Account Settings</Button>
  <Button on:click={tourModels}>Tour: Models</Button>
  <Button on:click={tourPipes}>Tour: Pipes</Button>
  <Button on:click={tourDriveGallery}>Tour: Drive Gallery</Button>
  <Button on:click={tourVisualizer}>Tour: Visualizer</Button>
  <Button on:click={tourTeams} class="col-span-2">Tour: Teams</Button>
</div>


{:else}
<div class="bg-highVizDark grid grid-cols-2 h-full w-full gap-3 py-2 text-white">
  <Button on:click={tourViewGallery}>Tour: Gallery</Button>
  <Button on:click={tourAccount}>Tour: Account Settings</Button>
  <Button on:click={tourModels}>Tour: Models</Button>
  <Button on:click={tourPipes}>Tour: Pipes</Button>
  <Button on:click={tourDriveGallery}>Tour: Drive Gallery</Button>
  <Button on:click={tourVisualizer}>Tour: Visualizer</Button>
  <Button on:click={tourTeams} class="col-span-2">Tour: Teams</Button>
</div>


{/if}


<style>
  .shepherd-theme-default, .shepherd-button {
    background: #1d72b8;
    color: white;
  }
</style>