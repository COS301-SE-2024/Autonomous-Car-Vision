
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
        <h1>Help Page</h1>
        <!-- Tour Manager component -->
        <TourManager />
      
        <!-- Add more buttons for other tours as needed -->
<!--       
        <Tour steps={activeTour} /> -->
      </div>
      
    {:else}
    <div class="help-page text-white">
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit text-xl font-medium" on:click={() => toggleTopic(0)}>
                    <span>View Gallery</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 0}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 0 ? 'open' : '' }">
                    <p class="m-2">On the Navigation bar, find and click the Gallery tab:</p>
                    <img src="./images/NavBar.png" alt="NavBar" class="screenshots" />
                    <p class="m-2">Once you do so, the Gallery page will open.</p>
                    <img src="./images/GalleryScreen.png" alt="Gallery" class="screenshots" />
                </div>
            </div>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit text-xl font-medium" on:click={() => toggleTopic(1)}>
                    <span>View/Download Video</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 1}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 1 ? 'open' : '' }">
                    <p class="m-2">Access the Gallery page. Click on a video of your choice.</p>
                    <img src="./images/GalleryScreen.png" alt="Gallery" class="screenshots" />
                    <p class="m-2"> If the video is not downloaded on your local machine, the download button will be visible </p>
                    <img src="./images/VideoNotDownloaded.png" alt="NotDownloaded" class="screenshots" />
                    <p>click on it to download the video from our server. Once downloaded, you can click on the video to view it and all the versions of which it was processed through models.</p>
                    <img src="./images/ViewVideoScreen.png" alt="VideoScreen" class="screenshots" />
                </div>
            </div>
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit text-xl font-medium" on:click={() => toggleTopic(2)}>
                    <span>Process Video</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 2}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 2 ? 'open' : '' }">
                    <p class="m-2">Access the video via the Gallery Page, and click on the Process Video button.</p>
                    <img src="./images/VideoViewScreen.png" alt="ViewVideo" class="screenshots" />
                    <p class="m-2"> This will open a modal window where you can select the model.  </p>
                    <img src="./images/ChooseModel.png" alt="ChooseModel" class="screenshots" />
                    <p class="m-2"> Confirm the model and wait patiently as the AI does its work.</p>
                    <img src="./images/ProcessConfirm.png" alt="VideoScreen" class="screenshots" />
                </div>
            </div>
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit text-xl font-medium" on:click={() => toggleTopic(3)}>
                    <span>View Models</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 3}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 3 ? 'open' : '' }">
                    <p class="m-2">On the Navigation bar, find and click the Models tab. </p>
                    <img src="./images/ModelsScreen.png" alt="ModelsScreen" class="screenshots" />
                    <p class="m-2" >To view more details of model, click the model to reveal the extended summary.</p>
                    <img src="./images/ModelContentScreen.png" alt="ModelContent" class="screenshots" />
                </div>
            </div>
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit text-xl font-medium" on:click={() => toggleTopic(4)}>
                    <span>Account Settings</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 4}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 4 ? 'open' : '' }">
                    <p class="m-2">Click on your username in the navigation bar. </p>
                    <img src="./images/AccountPopUp.png" alt="AccountPopUp" class="screenshots" />
                    <p class="m-2">  A pop-up menu will appear. Click on the Account Settings option to open the settings page.</p>
                    <img src="./images/AccountSettingsScreen.png" alt="AccountSettings" class="screenshots" />
                    <p class="m-2"> You can now edit your details</p>
                    <img src="./images/ChangePasswordScreen.png" alt="PasswordChange" class="screenshots" />
                </div>
            </div>
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit  text-white text-xl font-medium" on:click={() => toggleTopic(5)}>
                    <span>Search</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 5}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 5 ? 'open' : '' }">
                    <p class="m-2">Access any page with a search bar</p>
                    <img src="./images/GalleryScreen.png" alt="Gallery" class="screenshots" />
                    <p class="m-2" > Enter a keyword and wait for results to load.</p>
                    <img src="./images/EmptySearch.png" alt="Empty" class="screenshots" />
                    <img src="./images/successfulSearch.png" alt="Success" class="screenshots" />

                </div>
            </div>
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit  text-white text-xl font-medium" on:click={() => toggleTopic(6)}>
                    <span>Upload Video</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 6} ▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 6 ? 'open' : '' }">
                    <p class="m-2">Access the upload page from the Navigation Bar</p>
                    <img src="./images/UploadScreen.png" alt="Upload" class="screenshots" />
                    <p class="m-2" > Click on the upload slot and choose a video in your directory to upload.</p>
                    <img src="./images/UploadChoose.png" alt="Choose" class="screenshots" />
                    <p class="m-2" > Confirm your upload by clicking 'Save'. You will see the newly uploaded video in your Gallery page</p>
                    <img src="./images/UploadConfirm.png" alt="Confirm" class="screenshots" />
                </div>
            </div>
                
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit  text-white text-xl font-medium" on:click={() => toggleTopic(7)}>
                    <span>Drive Gallery</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 7} ▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 7 ? 'open' : '' }">
                    <p class="m-2">Access the Drive Gallery page from the Navigation Bar</p>
                    <img src="./images/DriveGalleryScreen.png" alt="DriveGallery" class="screenshots" />
                    <p class="m-2" > To view Drive Dashboard, click on any of the video.</p>
                    <img src="./images/DriveDashboard.png" alt="Dashboard" class="screenshots" />
                </div>
            </div>

            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit  text-white text-xl font-medium" on:click={() => toggleTopic(8)}>
                    <span>Pipes</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 8} ▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 8 ? 'open' : '' }">
                    <p class="m-2">Access the Pipes page from the Navigation Bar</p>
                    <img src="./images/PipesScreen.png" alt="Pipe" class="screenshots" />
                    <!-- Add more instructions on pipe interaction for demo 4 -->
                </div>
            </div>
            
            <div class="topic shadow-md shadow-theme-keith-accenttwo shadow-card">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="topic-title w-fit  text-white text-xl font-medium" on:click={() => toggleTopic(9)}>
                    <span>Logout</span>
                    <button class="dropdown-btn">
                        {#if $openTopic === 9}▲{:else}▼{/if}
                    </button>
                </div>
                <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 9 ? 'open' : '' }">
                    <p class="m-2">Click on your username in the navigation bar. A pop-up menu will appear; click on the Log Out button.</p>
                    <img src="./images/AccountPopUp.png" alt="Logout" class="screenshots" />
                </div>
            </div>
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
