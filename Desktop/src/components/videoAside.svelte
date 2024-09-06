<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { Avatar } from "svelte-materialify";
  import { get } from "svelte/store";
  import QuantamLoader from "./QuantamLoader.svelte";
  import {theme} from '../stores/themeStore';

  import {
    loadState,
    processing,
    originalVideoURL,
    videoUrl,
    remoteProcessingQueue,
  } from "../stores/processing";
  import { each } from "svelte/internal";

  export let AIinfo;

  let currrentVideoUrl;
  let mounting = true;
  let remoteProcessingQueueList = [];

  onMount(async () => {
    await loadState();
    currrentVideoUrl = get(videoUrl);

    let remoteQueue = get(remoteProcessingQueue);

    // Get video urls from the remote processing queue
    remoteQueue.forEach((detail) => {
      remoteProcessingQueueList.push(detail.outputVideoPath);
    });

    console.log("Remote Queue", remoteProcessingQueueList);

    if (remoteProcessingQueueList.includes(AIinfo.mURL)) {
      console.log("The list contains the URL.");
    } else {
      console.log("The list does not contain the URL.");
    }

    mounting = false;
  });

  const dispatch = createEventDispatcher();

  function selectVideo() {
    dispatch("select", AIinfo.mURL);
  }

  // Subscribe to remote processing queue
  remoteProcessingQueue.subscribe((value) => {
    let remoteQueue = value;

    remoteProcessingQueueList = [];

    // Get video urls from the remote processing queue
    remoteQueue.forEach((detail) => {
      remoteProcessingQueueList.push(detail.outputVideoPath);
    });
  });
</script>

{#if $theme === 'highVizLight'}
  <div class="component">
    <div class="flex flex-row justify-between items-center text-black">
      <Avatar size="42px">
        <img src={AIinfo.img} alt={AIinfo.mName} />
      </Avatar>
      <div class="xl:contents hidden">
        <a href="#/models">
          {AIinfo.mName}
        </a>
        <p>
          {AIinfo.mTime}
        </p>
      </div>
      <!-- <div
            class="flex flex-col justify-center items-center flex-nowrap"
            style="aspect-ratio: 16/9"
          >
            <QuantamLoader />
          </div> -->
      {#if mounting == false}
        {#if AIinfo.mURL != currrentVideoUrl}
          {#if remoteProcessingQueueList.includes(AIinfo.mURL)}
            <div
              class="flex flex-col justify-center items-center flex-nowrap"
              style="aspect-ratio: 14/7"
            >
              <QuantamLoader />
            </div>
          {:else}
            <button class="rounded border viewButtonLight" on:click={selectVideo}
              >View</button
            >
          {/if}
        {:else}
          <div
            class="flex flex-col justify-center items-center flex-nowrap"
            style="aspect-ratio: 14/7"
          >
            <QuantamLoader />
          </div>
        {/if}
      {/if}
    </div>
    <div class="lineLight"></div>
  </div>
{:else}
  <div class="component">
    <div class="flex flex-row justify-between items-center text-white">
      <Avatar size="42px">
        <img src={AIinfo.img} alt={AIinfo.mName} />
      </Avatar>
      <div class="xl:contents hidden">
        <a href="#/models">
          {AIinfo.mName}
        </a>
        <p>
          {AIinfo.mTime}
        </p>
      </div>
      <!-- <div
            class="flex flex-col justify-center items-center flex-nowrap"
            style="aspect-ratio: 16/9"
          >
            <QuantamLoader />
          </div> -->
      {#if mounting == false}
        {#if AIinfo.mURL != currrentVideoUrl}
          {#if remoteProcessingQueueList.includes(AIinfo.mURL)}
            <div
              class="flex flex-col justify-center items-center flex-nowrap"
              style="aspect-ratio: 14/7"
            >
              <QuantamLoader />
            </div>
          {:else}
            <button class="rounded border viewButton" on:click={selectVideo}
              >View</button
            >
          {/if}
        {:else}
          <div
            class="flex flex-col justify-center items-center flex-nowrap"
            style="aspect-ratio: 14/7"
          >
            <QuantamLoader />
          </div>
        {/if}
      {/if}
    </div>
    <div class="line"></div>
  </div>
{/if}



<style>
  a:hover {
    text-decoration: underline;
  }

  .component {
    padding-bottom: 20px;
  }

  .line {
    border-left: 2px solid rgba(255, 255, 255, 0.6);
    height: 20px;
    position: absolute;
    left: 20px;
  }

  .lineLight {
    border-left: 2px solid #0f6173c6;
    height: 20px;
    position: absolute;
    left: 20px;
  }

  .loaderDiv {
    width: 10%;
    height: 10%;
  }

  .viewButton {
    background-color: #1087a1c6;
    padding: 0.3rem;
  }


  .viewButtonLight {
    background-color: #0f6173c6;
    padding: 0.3rem;
  }

  .viewButton:hover {
    background-color: #0f6173c6;
  }

  .viewButtonLight:hover {
    background-color: #007ACC;
  }
</style>
