
<script>
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import { Avatar, Icon } from "svelte-materialify";
    import { mdiChevronDown } from '@mdi/js';
    import { writable } from 'svelte/store';


     const topics = [
        {
        title: 'View Gallery',
        details: 'Steps and screenshots to view the gallery...',
        },
        {
        title: 'View/Download Video',
        details: 'Steps and screenshots to view and download videos...',
        },
        {
        title: 'Process Video',
        details: 'Steps and screenshots to process videos...',
        },
        {
        title: 'View Models',
        details: 'Steps and screenshots to view models...',
        },
        {
        title: 'Account Settings',
        details: 'Steps and screenshots to manage account settings...',
        },
        {
        title: 'Logout',
        details: 'Steps and screenshots to logout...',
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
        <div class="topic">
        <div class="topic-title" on:click={() => toggleTopic(index)}>
            <span>{topic.title}</span>
            <button class="dropdown-btn">
            {#if $openTopic === index}▲{:else}▼{/if}
            </button>
        </div>
        <div class="topic-details { $openTopic === index ? 'open' : '' }">
            <p>{topic.details}</p>
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
</style>