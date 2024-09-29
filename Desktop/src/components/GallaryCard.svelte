<script>
  import { onMount } from "svelte";
  import { VideoURL, OriginalVideoURL } from "../stores/video";
  import { originalVideoURL } from "../stores/processing";
  import RingLoader from "./RingLoader.svelte";
  import { push } from "svelte-spa-router";
  import axios from "axios";
  import { mdiDownload, mdiPlayCircle } from "@mdi/js";
  import { Icon, Tooltip } from "svelte-materialify";
  import {theme } from "../stores/themeStore";

  export let videoSource;
  export let videoName;
  export let isDownloaded;
  export let listType;

  let isGalLoading = false;
  let showMoreModal = false;
  let firstFrameURL = "";
  let isDownloading = false;

  let showTooltip = false;
  let processed = false;

  const handleDownload = async (event) => {
    event.stopPropagation();
    // isDownloading.set(true);
    isDownloading = true;

    let uid = window.electronAPI.getUid();
    let token = window.electronAPI.getToken();
    let size = "10";
    let aip = "";
    let aport = "";

    try {
    let response = await window.electronAPI.openFTP(uid, token, size, "FAKENAME", "FAKEURL", "RETR");
    console.log("Response: ", response);
    
    if (response.success) {
        console.log("IP:", response.ip);
        console.log("Port:", response.port);
        aip = response.ip;
        aport = response.port;
    } else {
        console.error("Error:", response.error);
    }
} catch (error) {
    console.error("Error calling openFTP:", error);
}

    await window.electronAPI.downloadToClient(aip, aport, videoName, uid, size, token, videoSource);
    
    // move the video to the download folder
    let currentFilePath = videoName;
    console.log("Current File Path: ", currentFilePath);
    console.log("videoSource: ", videoSource);
 
    isDownloading = false;
      showMoreModal = false;
      isDownloaded = true;

    console.log("DOWNLOAD BUTTON");
  };

  function goToVideo() {
    if (!isDownloaded) return;
    console.log("Go to video");
    const encodedPath = encodeURIComponent(videoSource);
    VideoURL.set(videoSource);
    OriginalVideoURL.set(videoSource);
    originalVideoURL.set(videoSource);
    push(`/video/${encodedPath}`);
  }

  function handleMore() {
    console.log("More button clicked");
    showMoreModal = true;
    console.log(videoSource);
  }

  function handleBack(event) {
    console.log("Back button clicked");
    event.stopPropagation(); // Stop event propagation
    showMoreModal = false;
  }

  function captureSpecificFrame(frameNumber) {
    const videoElement = document.createElement("video");
    videoElement.src = videoSource;
    videoElement.crossOrigin = "anonymous"; // Ensure CORS is handled

    videoElement.addEventListener("loadedmetadata", () => {
      const fps = 30; // Assuming the video has 30 frames per second
      const targetTime = frameNumber / fps;

      videoElement.currentTime = targetTime;
    });

    videoElement.addEventListener("seeked", () => {
      if (videoElement.readyState >= 2) {
        // Ensure the video is loaded
        const canvas = document.createElement("canvas");
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        firstFrameURL = canvas.toDataURL("image/png");
        // Remove the video element from the DOM
        videoElement.remove();
      } else {
        console.error("Video is not ready to capture the frame.");
      }
    });
  }

  onMount(async () => {
    isGalLoading = true;
    captureSpecificFrame(10); // Specify the frame to get
    try {
      processed = await window.electronAPI.checkIfVideoProcessed(videoSource);
      console.log("Processed:", processed);
    } catch (error) {
      console.error("Error checking if video is processed:", error);
    }
    if (!isDownloaded) {
      try {
        const response = await window.electronAPI.getVideoFrame(
          videoSource,
          videoName
        );
        let videoPaths = response;
        firstFrameURL = videoPaths[0];
        console.log(firstFrameURL);
      } catch (error) {}
    }
    setInterval(() => {
      isGalLoading = false;
    }, 1500);
  });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
{#if $theme === 'highVizLight'}
  <div
  class="{isDownloaded
    ? 'cursor-default'
    : 'notDownloaded'} background-card relative overflow-hidden rounded-lg {listType === 'list' ? 'w-4/6 flex flex-row align-center justify-between' : 'w-11/12'} m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
  on:click={goToVideo}
  role="button"
  tabindex="0"
  >
  {#if isGalLoading}
    <div class="flex justify-center items-center h-64">
      <div class="content-loaderLight flex justify-center h-full w-full">
        <div class="img-content-loaderLight w-full">
          </div>
      </div>
    </div>
  {/if}
  {#if !isGalLoading}
    <div class="image-container relative">
      {#if listType === "grid"}
        <img
          src={firstFrameURL}
          alt="video preview"
          class="w-full object-cover aspect-video rounded-t-lg transition-filter duration-300 ease-in-out hover:filter-blur"
        />
      {:else}
        <img
        src={firstFrameURL}
        alt="video preview"
        class="w-28 object-cover aspect-video rounded-lg transition-filter duration-300 ease-in-out hover:filter-blur"
        />
      {/if}
      <div
        class="{isDownloaded
          ? 'hover:block'
          : 'hover:hidden'} lg:w-4/12 button-container absolute"
        style="top:40%; left:50%; transform: translate(-50%, 50%);"
      >
        {#if !isDownloading && !isDownloaded}
          <button
            class="more text-highVizLight-secondary-lightText w-full border-none px-2 py-1 rounded lg:text-md text-sm text-center justify-content-center display-flex align-items-center cursor-pointer"
            on:click={handleDownload}
          >
            <Icon path={mdiDownload} size="24" /></button
          >
        {:else if !isDownloaded}
          <div class="flex justify-center relative -top-4">
            <RingLoader />
          </div>
        {/if}
      </div>
      <div class="TT-positioning">
        <Tooltip left bind:active={showTooltip}>
          {#if listType === "grid"}
          <div
            class="processed-info"
            style={processed
              ? "background-color: #1AFF00;"
              : "background-color: red;"}
          ></div>
          {/if}
          <span slot="tip">
            {#if processed}
              Processed
            {:else}
              Unprocessed
            {/if}
          </span>
        </Tooltip>
      </div>
    </div>
    <div class="details p-2">
      <p
        class="details-link h-12 text-wrap overflow-hidden text-highVizLight-primary-lightText"
      >
        {videoName}
      </p>
      <div id="playbtn">
        <Icon
          class="text-highVizLight-secondary"
          path={mdiPlayCircle}
          size={40}
          on:click={goToVideo}
        />
      </div>
    </div>
  {/if}
  </div>
{:else}
  <div
  class="{isDownloaded
    ? 'cursor-default'
    : 'notDownloaded'} background-card relative overflow-hidden rounded-lg {listType === 'list' ? 'w-4/6 flex flex-row align-center justify-between' : 'w-11/12'} m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
  on:click={goToVideo}
  role="button"
  tabindex="0"
  >
  {#if isGalLoading}
    <div class="flex justify-center items-center h-64">
      <div class="content-loader flex justify-center h-full w-full">
        <div class="img-content-loader w-full">
          </div>
      </div>
    </div>
  {/if}
  {#if !isGalLoading}
    <div class="image-container relative">
      {#if listType === "grid"}
        <img
          src={firstFrameURL}
          alt="video preview"
          class="w-full object-cover aspect-video rounded-t-lg transition-filter duration-300 ease-in-out hover:filter-blur"
        />
      {:else}
        <img
        src={firstFrameURL}
        alt="video preview"
        class="w-28 object-cover aspect-video rounded-lg transition-filter duration-300 ease-in-out hover:filter-blur"
        />
      {/if}
      <div
        class="{isDownloaded
          ? 'hover:block'
          : 'hover:hidden'} lg:w-4/12 button-container absolute"
        style="top:40%; left:50%; transform: translate(-50%, 50%);"
      >
        {#if !isDownloading && !isDownloaded}
          <button
            class="more text-white-lightText w-full border-none px-2 py-1 rounded lg:text-md text-sm text-center justify-content-center display-flex align-items-center cursor-pointer"
            on:click={handleDownload}
          >
            <Icon path={mdiDownload} size="24" /></button
          >
        {:else if !isDownloaded}
          <div class="flex justify-center relative -top-4">
            <RingLoader />
          </div>
        {/if}
      </div>
      <div class="TT-positioning">
        <Tooltip left bind:active={showTooltip}>
          {#if listType === "grid"}
          <div
            class="processed-info"
            style={processed
              ? "background-color: #1AFF00;"
              : "background-color: red;"}
          ></div>
          {/if}
          <span slot="tip">
            {#if processed}
              Processed
            {:else}
              Unprocessed
            {/if}
          </span>
        </Tooltip>
      </div>
    </div>
    <div class="details p-2">
      <p
        class="details-link h-12 text-wrap overflow-hidden text-white"
      >
        {videoName}
      </p>
      <div id="playbtn">
        <Icon
          class="text-white"
          path={mdiPlayCircle}
          size={40}
          on:click={goToVideo}
        />
      </div>
    </div>
  {/if}
  </div>
{/if}


<style>
  img {
    aspect-ratio: 16/9;
  }
  .content-loader {
    background-color: #25292b;
    border-radius: 10px;
    animation: pulse 1.5s infinite;
  }

  .content-loaderLight {
    background-color: #8ec5dd;
    border-radius: 10px;
    animation: pulse 1.5s infinite;
  }

  .img-content-loader {
    background-color: #3d3d3d;
    border-radius: 10px;
    height: 83.333%;
    animation: pulse 1.5s infinite;
  }

  .img-content-loaderLight {
    background-color: #B6D9E8;
    border-radius: 10px;
    height: 83.333%;
    animation: pulse 1.5s infinite;
  }

  .TT-positioning {
    position: absolute;
    top: 5px;
    right: 12px;
  }

  .processed-info {
    width: 12px;
    height: 12px;
    color: white;
    border-radius: 50%;
  }

  .notDownloaded {
    filter: grayscale(100%);
    cursor: pointer;
    shadow: grayscale;
  }

  .cursor-default {
    cursor: default;
  }

  .details {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  #playbtn {
    height: fit-content;
    cursor: pointer;
  }

  .background-card {
    /* border: 0.5px solid #012431; */
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  }

  .background-card:hover {
    background-color: #012431b1;
  }
</style>
