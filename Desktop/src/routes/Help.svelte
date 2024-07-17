<!-- 
<script>
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import { Avatar, Icon } from "svelte-materialify";
    import { mdiChevronDown } from '@mdi/js';
    import { writable } from 'svelte/store';


     const topics = [
        {
        title: 'View Gallery',
        details: 'On the Navigation bar, find and click the Gallery tab: ',
        images: ['https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/NavBar.png'],
        },
        {
        title: 'View/Download Video',
        details: 'Access the Gallery page. Click on a video of your choice. If the video is not downloaded on your local machine, the download button will be visible; click on it to download the video from our server. Once downloaded, you can click on the video to view it and all the versions of which it was processed through models.',
        images: ['Documentation/Images/HelpImages/ChosenVideo.png']
        },
        {
        title: 'Process Video',
        details: 'After you have uploaded the video, click on the Process Video button. This will open a modal window where you can select the model. Confirm the model and wait patiently as the AI does its work.',
        images: ['https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ChosenVideo.png', 'https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ProcessPopUp.png', 'https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ProcessingLoader.png'],
        },
        {
        title: 'View Models',
        details: 'On the Navigation bar, find and click the Models tab. To view more details of model, simply hover over it to reveal the extended summary. ',
        images: ['https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ModelsPage.png', 'https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/FliipedModelCard.png'],
        }
        ,
        {
        title: 'Account Settings',
        details: 'Click on your username in the navigation bar. A pop-up menu will appear. Click on the Account Settings option to open the settings page.',
        images: ['https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/SettingsPopUp.png', 'https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/AccountSettings.png'],
        },
        {
        title: 'Logout',
        details: 'Click on your username in the navigation bar. A pop-up menu will appear; click on the Log Out button',
        images: ['https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/AccountSettings.png'],
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
            {#each topic.images as image}
            <img src={image} alt="screenshot" class="screenshots" />
            {/each}
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
        display:block;
        align-content: center;
        align-items: center;
        justify-content: center;
        padding-left: 10px;
        align-self: center;
    }
</style> -->

<script>
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import { writable } from 'svelte/store';

    // Store for tracking the open topic index
    const openTopic = writable(null);

    // Function to toggle the topic details view
    function toggleTopic(index) {
        openTopic.update((current) => (current === index ? null : index));
    }

    let NavBarImg = "https://drive.google.com/file/d/1R149vbVOIvFrYllmcYnbw1AnQxvIWkc8/view?usp=drive_link";
</script>

<ProtectedRoutes>
    <div class="help-page">
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(0)}>
                <span>View Gallery</span>
                <button class="dropdown-btn">
                    {#if $openTopic === 0}▲{:else}▼{/if}
                </button>
            </div>
            <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 0 ? 'open' : '' }">
                <p>On the Navigation bar, find and click the Gallery tab:</p>
                <img src="/public/images/NavBar.png" alt="NavBar" class="screenshots" />
            </div>
        </div>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(1)}>
                <span>View/Download Video</span>
                <button class="dropdown-btn">
                    {#if $openTopic === 1}▲{:else}▼{/if}
                </button>
            </div>
            <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 1 ? 'open' : '' }">
                <p>Access the Gallery page. Click on a video of your choice. If the video is not downloaded on your local machine, the download button will be visible; click on it to download the video from our server. Once downloaded, you can click on the video to view it and all the versions of which it was processed through models.</p>
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/develop/Documentation/Images/HelpImages/ChosenVideo.png?raw=true" alt="chosen" class="screenshots" />
            </div>
        </div>
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(2)}>
                <span>Process Video</span>
                <button class="dropdown-btn">
                    {#if $openTopic === 2}▲{:else}▼{/if}
                </button>
            </div>
            <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 2 ? 'open' : '' }">
                <p>After you have uploaded the video, click on the Process Video button. This will open a modal window where you can select the model. Confirm the model and wait patiently as the AI does its work.</p>
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ChosenVideo.png" alt="screenshot" class="screenshots" />
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ProcessPopUp.png" alt="screenshot" class="screenshots" />
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ProcessingLoader.png" alt="screenshot" class="screenshots" />
            </div>
        </div>
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(3)}>
                <span>View Models</span>
                <button class="dropdown-btn">
                    {#if $openTopic === 3}▲{:else}▼{/if}
                </button>
            </div>
            <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 3 ? 'open' : '' }">
                <p>On the Navigation bar, find and click the Models tab. To view more details of model, simply hover over it to reveal the extended summary.</p>
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/ModelsPage.png" alt="screenshot" class="screenshots" />
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/FliipedModelCard.png" alt="screenshot" class="screenshots" />
            </div>
        </div>
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(4)}>
                <span>Account Settings</span>
                <button class="dropdown-btn">
                    {#if $openTopic === 4}▲{:else}▼{/if}
                </button>
            </div>
            <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 4 ? 'open' : '' }">
                <p>Click on your username in the navigation bar. A pop-up menu will appear. Click on the Account Settings option to open the settings page.</p>
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/SettingsPopUp.png" alt="screenshot" class="screenshots" />
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/develop/Documentation/Images/HelpImages/AccountSettings.png" alt="screenshot" class="screenshots" />
            </div>
        </div>
        <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card-blue">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(5)}>
                <span>Logout</span>
                <button class="dropdown-btn">
                    {#if $openTopic === 5}▲{:else}▼{/if}
                </button>
            </div>
            <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 5 ? 'open' : '' }">
                <p>Click on your username in the navigation bar. A pop-up menu will appear; click on the Log Out button.</p>
                <img src="https://github.com/COS301-SE-2024/Autonomous-Car-Vision/blob/feature/help_fix2/Documentation/Images/HelpImages/AccountSettings.png" alt="screenshot" class="screenshots" />
            </div>
        </div>
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

    .screenshots {
        display: block;
        align-items: center;
        justify-content: center;
        /* padding-left: 10px; */
        width: 370px;
        height: 240px;
    }
</style>
