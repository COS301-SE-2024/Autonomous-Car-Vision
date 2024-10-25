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
      videoPath = get(originalVideoURL);
      appPath = await window.electronAPI.getAppPath();
      const videoName = getFileName(videoPath);
      videoNameExtract = videoName.split(".")[0];

      const outputDir = `${appPath}/outputVideos/${videoNameExtract}`;
      const files = await window.electronAPI.readDirectory(outputDir);

      let originalVideo = await window.electronAPI.getVideoByURL(videoPath);

      if (!originalVideo) {
        const newOriginalVideo = {
          label: "Original",
          profileImgURL: "https://placekitten.com/300/300",
          videoURL: videoPath,
          originalVidID: null,
        };
        originalVideo = await window.electronAPI.addVideo(newOriginalVideo);

        originalVideo = await window.electronAPI.getVideoByURL(videoPath);
        if (!originalVideo) {
          throw new Error("Failed to add original video to the database");
        }
      }

      processedVideos = [
        {
          id: originalVideo.videoID,
          label: "Original",
          profileImgURL: originalVideo.profileImgURL,
          videoURL: originalVideo.videoURL,
        },
      ];

      const processedVideoEntries = await window.electronAPI.getProcessedVideos(
        originalVideo.videoID
      );

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

  processing.subscribe((value) => {
    processingVideo = value;
  });

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
    {/each}
  </div>
{/if}
