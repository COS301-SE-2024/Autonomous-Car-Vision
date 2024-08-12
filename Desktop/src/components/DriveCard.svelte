<script>
  import { onMount } from "svelte";
  import { VideoURL, OriginalVideoURL } from "../stores/video";
  import { originalVideoURL } from "../stores/processing";
  import RingLoader from "./RingLoader.svelte";
  import { push } from "svelte-spa-router";
  import { mdiDownload, mdiPlayCircle } from "@mdi/js";
  import { Icon, Tooltip } from "svelte-materialify";

  export let videoSource;
  export let videoName;
  export let listType;

  let isGalLoading = false;
  let firstFrameURL = "";

  let showTooltip = false;
  let processed = false;

  function goToVideo() {
    console.log("Go to video");
    const encodedPath = encodeURIComponent(videoSource);
    VideoURL.set(videoSource);
    OriginalVideoURL.set(videoSource);
    originalVideoURL.set(videoSource);
    console.log(encodedPath);
    push(`/drive/${encodedPath}`);
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
    captureSpecificFrame(1);

    try {
      processed = await window.electronAPI.checkIfVideoProcessed(videoSource);
      console.log("Processed:", processed);
    } catch (error) {
      console.error("Error checking if video is processed:", error);
    }
    // Other fetching logic

    setInterval(() => {
      isGalLoading = false;
    }, 1500);
  });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
  class="background-card text-white relative overflow-hidden rounded-lg {listType !==
  'grid'
    ? 'w-5/6 flex flex-row align-center justify-between'
    : 'w-10/12 mx-auto'} 
    m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
  on:click={goToVideo}
  role="button"
  tabindex="0"
>
  {#if isGalLoading}
    <div class="flex justify-center items-center h-64">
      <div class="content-loader flex justify-center h-full w-full">
        <div class="img-content-loader w-full"></div>
      </div>
    </div>
  {/if}
  {#if !isGalLoading}
    <div class="image-container relative h-auto">
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
        class="lg:w-4/12 button-container absolute"
        style="top:40%; left:50%; transform: translate(-50%, 50%);"
      >
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
        class="details-link h-12 text-wrap overflow-hidden text-theme-dark-lightText"
      >
        {videoName}
      </p>
    </div>
  {/if}
</div>

<style>
  img {
    aspect-ratio: 16/9;
  }

  .content-loader {
    background-color: #25292b;
    border-radius: 10px;
    animation: pulse 1.5s infinite;
  }

  .img-content-loader {
    background-color: #3d3d3d;
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

  .details {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .background-card {
    /* border: 0.5px solid #012431; */
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  }

  .background-card:hover {
    background-color: #012431b1;
  }
</style>
