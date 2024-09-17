<script>
    import Shepherd from 'shepherd.js';
    import {theme} from '../stores/themeStore';
    import { push } from "svelte-spa-router"; // Assuming you're using svelte-routing for navigation
  
   // Function to initialize a basic tour
  function initTour(steps) {
    const tour = new Shepherd.Tour({
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

  // Tour: Changing Password
  function tourChangePassword() {
    const steps = [
      {
        id: 'go-to-profile',
        text: 'First, go to your profile page.',
        attachTo: { element: '#profile-nav', on: 'bottom' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/profile');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'find-password-change',
        text: 'Here you can find the "Change Password" option.',
        attachTo: { element: '#change-password-btn', on: 'right' },
        buttons: [
          {
            text: 'Next',
            action: () => tour.next()
          }
        ]
      },
      {
        id: 'enter-password',
        text: 'Enter your new password here.',
        attachTo: { element: '#password-field', on: 'right' },
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

  // Tour: Accessing Home Page
  function tourViewGallery() {
    const steps = [
      {
        id: 'go-to-gallery',
        text: 'Click here to go to the gallery page.',
        attachTo: { element: '#home-nav', on: 'bottom' },
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
        id: 'home-overview',
        text: 'This is the main overview of your gallery page.',
        attachTo: { element: '#home-overview', on: 'top' },
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

  // Tour: Editing User Profile
  function tourEditProfile() {
    const steps = [
      {
        id: 'go-to-profile',
        text: 'First, go to your profile page.',
        attachTo: { element: '#profile-nav', on: 'bottom' },
        buttons: [
          {
            text: 'Next',
            action: () => {
              push('/profile');  // Navigating using svelte-spa-router
              tour.next();
            }
          }
        ]
      },
      {
        id: 'edit-profile',
        text: 'Click here to edit your profile.',
        attachTo: { element: '#edit-profile-btn', on: 'right' },
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
</script>

{#if $theme === 'highVizLight'}
<div>
  <h1>Help Page</h1>
  <button on:click={tourChangePassword}>Tour: Changing Password</button>
  <button class=".shepherd-button " on:click={tourViewGallery}>Tour: Accessing Home Page</button>
  <button on:click={tourEditProfile}>Tour: Editing User Profile</button>
</div>


{:else}
<div>
  <h1>Help Page</h1>
  <button  on:click={tourChangePassword}>Tour: Changing Password</button>
  <button on:click={tourViewGallery}>Tour: Accessing Home Page</button>
  <button on:click={tourEditProfile}>Tour: Editing User Profile</button>
</div>


{/if}


<style>
  .shepherd-theme-default, .shepherd-button {
    background: #1d72b8;
    color: white;
  }
</style>