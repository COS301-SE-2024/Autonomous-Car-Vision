<script>
  import { createEventDispatcher, onMount } from "svelte";
  import GallaryMore from "./GallaryMore.svelte";

  export let VideoSource;

  let showMoreModal = false;
  let firstFrameURL = "";
  let isDownloaded = false;
  const dispatch = createEventDispatcher();

  function handleDownload() {
    // Logic to download the video
    isDownloaded = true;
  }

  function handleMore() {
    console.log("More button clicked");
    showMoreModal = true;
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

    videoElement.addEventListener("error", (e) => {
      console.error("Error loading video: ", e);
    });

    // Add the video element to the DOM to trigger loading
    document.body.appendChild(videoElement);
  }

  onMount(() => {
    captureSpecificFrame(10); // Specify the frame to get
  });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
{#if isDownloaded}
  <div
    class="relative overflow-hidden rounded-lg p-2 w-48 shadow-md shadow-theme-keith-accenttwo m-2 transition-all duration-300 ease-in-out"
    on:click={handleMore}
  >
    <div class="image-container relative">
      <img
        src={firstFrameURL}
        alt="video preview"
        class="w-full rounded-lg transition-filter duration-300 ease-in-out hover:filter-blur"
      />
      <div
        class="button-container absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden"
      >
        <button
          class="more bg-blue text-white border-none px-2 py-1 rounded text-xs"
          on:click={handleMore}>More</button
        >
      </div>
    </div>
    <div class="details p-2">
      <p class="details-link">Details here...</p>
    </div>
  </div>
{:else}
  <div
    class="relative overflow-hidden rounded-lg p-2 w-48 shadow-md shadow-theme-keith-accenttwo m-2 transition-all duration-300 ease-in-out"
    on:click={handleMore}
  >
    <div class="image-container relative filter grayscale">
      <img
        src={firstFrameURL}
        alt="video preview"
        class="w-full rounded-lg transition-filter duration-300 ease-in-out"
      />
      <div
        class="button-container absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hidden"
      >
        <button
          class="download bg-blue text-white border-none px-2 py-1 rounded text-xs"
          on:click={handleDownload}>Download</button
        >
      </div>
    </div>
    <div class="details p-2">
      <p class="details-link">Details here...</p>
    </div>
  </div>
{/if}

{#if showMoreModal}
<div>
  <GallaryMore imgSource={firstFrameURL} videoSource={VideoSource} on:close={handleBack} />
</div>
{/if}

<style>
</style>
