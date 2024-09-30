<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { get } from "svelte/store";
  import { VideoURL, OriginalVideoURL } from "../stores/video";
  import {
    loadState,
    processing,
    originalVideoURL,
    videoUrl,
  } from "../stores/processing";

  const dispatch = createEventDispatcher();

  let processedVideos = [];
  let processingVideo;
  let currrentVideoUrl;
  let appPath = "";
  let videoPath;
  let videoNameExtract = "";

  let mounting = true;

  onMount(async () => {
    await loadState();
    processingVideo = get(processing);
    currrentVideoUrl = get(videoUrl);

    await getOutputFiles();

    mounting = false;
  });

  async function getOutputFiles() {
    try {
      // Fetch video details
      videoPath = get(originalVideoURL);
      appPath = await window.electronAPI.getAppPath();
      const videoName = getFileName(videoPath);
      videoNameExtract = videoName.split(".")[0];

      const outputDir = `${appPath}/outputVideos/${videoNameExtract}`;
      const files = await window.electronAPI.readDirectory(outputDir);

      // Fetch the original video details from the database
      let originalVideo = await window.electronAPI.getVideoByURL(videoPath);

      // If the original video is not found, add it to the database
      if (!originalVideo) {
        const newOriginalVideo = {
          label: "Original",
          profileImgURL: "https://placekitten.com/300/300",
          videoURL: videoPath,
          originalVidID: null, // Set to null instead of 0
        };
        originalVideo = await window.electronAPI.addVideo(newOriginalVideo);

        // Fetch the original video again to get the complete data including ID
        originalVideo = await window.electronAPI.getVideoByURL(videoPath);
        if (!originalVideo) {
          throw new Error("Failed to add original video to the database");
        }
      }

      // Start with the original video
      processedVideos = [
        {
          id: originalVideo.videoID,
          label: "Original",
          profileImgURL: originalVideo.profileImgURL,
          videoURL: originalVideo.videoURL,
        },
      ];

      // Fetch processed videos linked to the original video
      const processedVideoEntries = await window.electronAPI.getProcessedVideos(
        originalVideo.videoID
      );

      // Add processed videos
      processedVideoEntries.forEach((video) => {
        processedVideos.push({
          id: video.videoID,
          label: video.label,
          profileImgURL: video.profileImgURL,
          videoURL: video.videoURL,
        });
      });
    } catch (error) {
      console.error("Error fetching output files:", error);
    }
  }

  function getFileName(filePath) {
    const parts = filePath.split(/[/\\]/);
    return parts[parts.length - 1];
  }

  function selectModel(model) {
    dispatch("select", model);
  }

  // Subscripe to the processing store
  processing.subscribe((value) => {
    processingVideo = value;
  });

  // Subscribe to the videoUrl store
  videoUrl.subscribe((value) => {
    currrentVideoUrl = value;
  });
</script>

{#if mounting == false}
  <div
    class="absolute top-0 right-0 bg-theme-dark-white border border-theme-dark-backgroundBlue g p-4 z-50 flex flex-col rounded-lg"
  >
    {#each processedVideos as video}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      {#if video.videoURL != currrentVideoUrl}
        <div
          class="mb-2 cursor-pointer flex items-center rounded border-b border-theme-dark-primary text-black"
          on:click={() => selectModel(video)}
        >
          <img
            src={video.profileImgURL}
            alt="Model Profile"
            class="w-12 h-12 rounded-full mr-2"
          />
          <p class="text-xs text-black">{video.label}</p>
        </div>
      {:else}
        <div
          class="mb-2 cursor-pointer flex items-center rounded border-b border-theme-dark-primary text-black"
        >
          <img
            src={video.profileImgURL}
            alt="Model Profile"
            class="w-12 h-12 rounded-full mr-2"
          />
          <p class="text-xs text-black">Processing...</p>
        </div>
      {/if}

      <!-- <div class="mb-2 cursor-pointer flex items-center rounded border-b border-theme-dark-primary text-black" on:click={() => selectModel(video)}>
        <img src={video.profileImgURL} alt="Model Profile" class="w-12 h-12 rounded-full mr-2">
        <p class="text-xs text-black">{video.label}</p>
      </div> -->
    {/each}
  </div>
{/if}
