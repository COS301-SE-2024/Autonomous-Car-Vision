<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { Avatar } from "svelte-materialify";
  import { get } from "svelte/store";
  import QuantamLoader from "./QuantamLoader.svelte";

  import {
    loadState,
    processing,
    originalVideoURL,
    videoUrl,
  } from "../stores/processing";

  export let AIinfo;

  let currrentVideoUrl;
  let mounting = true;

  onMount(async () => {
    await loadState();
    currrentVideoUrl = get(videoUrl);

    mounting = false;
  });

  const dispatch = createEventDispatcher();

  function selectVideo() {
    dispatch("select", AIinfo.mURL);
  }
</script>

<div class="component">
  <div class="flex flex-row justify-between items-center text-white">
    <Avatar size="42px">
      <img src={AIinfo.img} alt={AIinfo.mName} />
    </Avatar>
    <a href="#/models">
      {AIinfo.mName}
    </a>
    <p>
      {AIinfo.mTime}
    </p>
    <!-- <div
          class="flex flex-col justify-center items-center flex-nowrap"
          style="aspect-ratio: 16/9"
        >
          <QuantamLoader />
        </div> -->
    {#if mounting == false}
      {#if AIinfo.mURL != currrentVideoUrl}
        <button class="rounded border viewButton" on:click={selectVideo}
          >View</button
        >
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

  .loaderDiv {
    width: 10%;
    height: 10%;
  }

  .viewButton {
    background-color: #1087a1c6;
    padding: 0.3rem;
  }

  .viewButton:hover {
    background-color: #0f6173c6;
  }
</style>
