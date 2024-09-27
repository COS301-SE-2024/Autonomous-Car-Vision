
<script>
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import { writable } from 'svelte/store';
    import {theme} from '../stores/themeStore';
    // import { tours } from './tours/tours';
    // import { Tour } from 'svelte-tour';
     import TourManager from '../components/TourManager.svelte';

    let activeTour = [];

    function startTour(tourName) {
        activeTour = tours[tourName] || [];
    }

    // Store for tracking the open topic index
    const openTopic = writable(null);

    // Function to toggle the topic details view
    function toggleTopic(index) {
        openTopic.update((current) => (current === index ? null : index));
    }

</script>

<ProtectedRoutes>
    {#if $theme === 'highVizLight'}
    <div>
        <h1 class="pt-5 headerLight text-xl items-center text-center">Help Menu</h1>
        <br>
        <br>
        <!-- Tour Manager component -->
        <TourManager />
      </div>
      
    {:else}
    <div>
        <h1 class="pt-5 headerDark text-white text-xl items-center text-center">Help Menu</h1>
        <br>
        <br>
        <!-- Tour Manager component -->
        <TourManager />
      </div>
    {/if}

    
</ProtectedRoutes>

<style>
    .help-page {
        max-height: 100vh;
        overflow-y: auto;
        padding: 20px;
        box-sizing: border-box;
    }

    .topic {
        border: 1px solid #ccc;
        border-radius: 8px;
        margin-bottom: 10px;
        padding: 10px;
        position: relative;
    }

    .topicLight {
        border: 1px solid #0099FF;
        border-radius: 8px;
        margin-bottom: 10px;
        padding: 10px;
        position: relative;
    }

    .topic-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }

    .topic-details {
        margin-top: 10px;
        display: none;
    }

    .topic-details.open {
        display: block;
    }

    .dropdown-btn {
        background: none;
        border: none;
        font-size: 16px;
        cursor: pointer;
    }

    .screenshots {
        display: block;
        align-items: center;
        justify-content: center;
        /* padding-left: 10px; */
        width: 380px;
        height: 210px;
        max-width: 100%;
        max-height: 100%;
        margin: 1rem;
    }
</style>
