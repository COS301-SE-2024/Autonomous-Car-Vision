
<script>
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import { Avatar, Icon } from "svelte-materialify";
    import { mdiChevronDown } from '@mdi/js';
    import { writable } from 'svelte/store';


     const topics = [
        {
        title: 'View Gallery',
        details: 'On the Navigation bar, find and click the Gallery tab: ',
        images: '<Screenshot>',
        },
        {
        title: 'View/Download Video',
        details: 'Access the Gallery page. Click on a video of your choice. If the video is not downloaded on your local machine, the download button will be visible; click on it to download the video from our server. Once downloaded, you can click on the video to view it and all the versions of which it was processed through models.',
        images: '<Screenshots>',
        },
        {
        title: 'Process Video',
        details: 'Steps and screenshots to process videos...',
        images: '<Screenshot>',
        },
        {
        title: 'View Models',
        details: 'On the Navigation bar, find and click the Models tab. To view more details of model, simply hover over it to reveal the extended summary. ',
        images: '<Screenshot>',
        }
        ,
        {
        title: 'Account Settings',
        details: 'Click on your username in the navigation bar. A pop-up menu will appear. Click on the Account Settings option to open the settings page.',
        images: '<Screenshot>',
        },
        {
        title: 'Logout',
        details: 'Click on your username in the navigation bar. A pop-up menu will appear; click on the Log Out button',
        images: '<Screenshot>',
        },
    ];

    const openTopic = writable(null);

    const items = [
    { name: "Open", iconPath: mdiChevronDown },
  ];

   function toggleTopic(index) {
    openTopic.update((current) => (current === index ? null : index));
  }
</script>

<ProtectedRoutes>
   <div class="help-page">
    {#each topics as topic, index}
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue ">
        <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(index)}>
            <span>{topic.title}</span>
            <button class="dropdown-btn">
            {#if $openTopic === index}▲{:else}▼{/if}
            </button>
        </div>
        <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === index ? 'open' : '' }">
            <p>{topic.details}</p> <br>
            <p class="screenshots text-light pr-10" >{topic.images} </p>
            <!-- Insert screenshots and detailed steps here -->
        </div>
        </div>
    {/each}
    </div>
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

    .screenshots{
        display:flex;
        align-text: center;
        align-items: center;
        justify-content: center;
        
    }
</style>