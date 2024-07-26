<script>
  import { onMount } from "svelte";
  import GallaryMore from "./GallaryMore.svelte";
  import PingLoader from "../components/PingLoader.svelte";
  import { VideoURL, OriginalVideoURL } from "../stores/video";
  import { writable } from "svelte/store";
  import { originalVideoURL } from "../stores/processing";
  import { get } from 'svelte/store';
  import RingLoader from "./RingLoader.svelte";
  import { push } from "svelte-spa-router";
  import { mdiDownload, mdiPlayCircle } from "@mdi/js";
  import { Icon, Tooltip } from "svelte-materialify";

  export let VideoSource;
  export let VideoName;
  export let isDownloaded;

  let isGalLoading = false;
  let showMoreModal = false;
  let firstFrameURL = "";
  let isDownloading = false;

  let showTT = false;
  let processed = true;

  const handleDownload = async (event) => {
    event.stopPropagation();
    // isDownloading.set(true);
    isDownloading = true;
    try {
      const response = await window.electronAPI.downloadVideo(
        VideoName,
        VideoSource,
      );
      console.log(response.success, response.filePath);
    } catch (error) {}
    setTimeout(() => {
      // isDownloading.set(false);
      isDownloading = false;
      showMoreModal = false;
      isDownloaded = true;
    }, 10000);
    console.log("DOWNLOAD BUTTON");
  };

  function goToVideo() {
    if (!isDownloaded) return;
    console.log("Go to video");
    const encodedPath = encodeURIComponent(VideoSource);
    VideoURL.set(VideoSource);
    push(`/video/${encodedPath}`);
  }

  function handleMore() {
    console.log("More button clicked");
    showMoreModal = true;
    console.log(VideoSource);
  }

  function handleBack(event) {
    console.log("Back button clicked");
    event.stopPropagation(); // Stop event propagation
    showMoreModal = false;
  }

  function captureSpecificFrame(frameNumber) {
    const videoElement = document.createElement("video");
    videoElement.src = VideoSource;
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
    if (!isDownloaded) {
      try {
        const response = await window.electronAPI.getVideoFrame(
          VideoSource,
          VideoName,
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
<div
  class="{isDownloaded
    ? 'cursor-default'
    : 'notDownloaded'} background-card shadow-card-blue relative overflow-hidden rounded-lg p-2 w-10/12 shadow-theme-keith-accenttwo m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
  on:click={goToVideo}
>
  {#if isGalLoading}
    <div class="flex justify-center items-center h-64">
      <div class="flex justify-center">
        <PingLoader />
      </div>
    </div>
  {/if}
  {#if !isGalLoading}
    <div class="image-container relative">
      <img
        src={firstFrameURL}
        alt="video preview"
        class="h-64 w-full object-cover aspect-video rounded-lg transition-filter duration-300 ease-in-out hover:filter-blur"
      />
      <div
        class="{isDownloaded
          ? 'hover:block'
          : 'hover:hidden'} lg:w-4/12 button-container absolute"
        style="top:40%; left:50%; transform: translate(-50%, 50%);"
      >
        {#if !isDownloading && !isDownloaded}
          <button
            class="more text-theme-dark-lightText w-full border-none px-2 py-1 rounded lg:text-md text-sm text-center justify-content-center display-flex align-items-center cursor-pointer"
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
        <Tooltip left bind:active={showTT}>
          <div
            class="processed-info"
            style={processed
              ? "background-color: green;"
              : "background-color: red;"}
          ></div>
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
        class="details-link h-12 text-wrap overflow-hidden text-theme-dark-lightText"
      >
        {VideoName}
      </p>
      <div id="playbtn">
        <Icon
          class="text-dark-secondary"
          path={mdiPlayCircle}
          size={40}
          on:click={goToVideo}
        />
      </div>
    </div>
  {/if}
</div>

<style>
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
  }

  #playbtn {
    height: fit-content;
    cursor: pointer;
  }

  .background-card {
    background-color: #01243150;
  }
</style>
