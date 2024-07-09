<script>
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { fly } from "svelte/transition";
  import { location } from "svelte-spa-router";
  import { VideoURL } from "../stores/video";
  import { Avatar, Button, Icon } from "svelte-materialify";
  import {
    mdiPause,
    mdiPlay,
    mdiReplay,
    mdiMenuLeftOutline,
    mdiMenuRightOutline,
  } from "@mdi/js";

  import {
    loadState,
    originalVideoURL,
    processing,
    videoUrl,
  } from "../stores/processing";

  import VideoAside from "./videoAside.svelte";
  import { each } from "svelte/internal";

  export let videoPath;

  let time = 0;
  let volume = 0;
  let duration;
  let paused = true;

  let showControls = true;
  let showControlsTimeout;

  let thumbnailBar;
  let frames = [];
  let ended = false;
  let showSideAIDetail = false;

  let processedVideos = [];
  let processingVideo;
  let currrentVideoUrl;
  let appPath = "";
  let originalVideoPath;
  let videoNameExtract = "";

  let AIinfoDone = false;

  function format(seconds) {
    if (isNaN(seconds)) return "...";
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    seconds = Math.floor(seconds % 60);
    if (seconds < 10) seconds = "0" + seconds;
    if (minutes < 10 || null) minutes = "0" + minutes;
    if (hours < 10 || null) hours = "0" + hours;

    if (hours == 0 || null) {
      return `${minutes}:${seconds}`;
    } else return `${hours}:${minutes}:${seconds}`;
  }

  let lastMouseDown;

  function handleMouseEnter(e) {
    // Clear any existing timeout to prevent the controls from hiding
    clearTimeout(showControlsTimeout);
    // Show the controls immediately
    showControls = true;
  }

  function handleMouseLeave(e) {
    // Start the timeout to hide the controls after 2500ms
    showControlsTimeout = setTimeout(() => (showControls = false), 2500);
  }

  function handleMove(e) {
    clearTimeout(showControlsTimeout);
    showControlsTimeout = setTimeout(() => (showControls = false), 2500);
    showControls = true;

    if (!duration) return;
    if (e.type !== "touchmove" && !(e.buttons & 1)) return;

    const clientX = e.type === "touchmove" ? e.touches[0].clientX : e.clientX;
    const { left, right } = this.getBoundingClientRect();
    time = (duration * (clientX - left)) / (right - left);

    // Find the frame index that corresponds to the current time
    const frameIndex = Math.floor((time / duration) * frames.length);
    const frameElement = document.querySelectorAll(".thumbnail")[frameIndex];
    if (frameElement) {
      frameElement.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center",
      });
    }
  }

  function handleMousedown(e) {
    lastMouseDown = new Date();
  }

  function handleMouseup(e) {
    if (new Date() - lastMouseDown < 300) {
      if (paused) e.target.play();
      else e.target.pause();
    }
    // Find the frame index that corresponds to the current time
    const frameIndex = Math.floor((time / duration) * frames.length);
    const frameElement = document.querySelectorAll(".thumbnail")[frameIndex];
    if (frameElement) {
      frameElement.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center",
      });
    }
  }

  async function extractFrames() {
    try {
      const framePaths = await window.electronAPI.extractFrames(videoPath);
      frames = framePaths.map((framePath) => framePath.replace(/\\/g, "/")); // Convert backslashes to slashes for URLs
      console.log("Video Path: ", videoPath);
    } catch (error) {
      console.error("Error extracting frames:", error);
    }
  }

  // Subscribe to the videoURL store to get the clicked video
  $: VideoURL.subscribe((value) => {
    videoPath = value;
  });

  onMount(async () => {
    console.log($location);
    // const encodedPath = encodeURIComponent(VideoSource);
    videoPath = $location.replace("/video/", "");
    videoPath = decodeURIComponent(videoPath);
    console.log("VideoPath: ", videoPath);
    console.log("Stores: ", $VideoURL);
    extractFrames();
    await loadState();
    await getAIinfo();

    AIinfoDone = true;
  });

  function seekToFrame(framePath) {
    const index = frames.indexOf(framePath);
    time = index * (duration / frames.length); // Adjust according to the interval
    console.log("Seek to frame:", framePath);
    showControls = true;

    // Scroll the clicked frame into the center of the thumbnail bar
    const frameElement = document.querySelectorAll(".thumbnail")[index];
    if (frameElement) {
      frameElement.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center",
      });
    }
  }

  function pause() {
    if (ended) {
      time = 0;
      return;
    }
    paused = !paused;
  }

  function handleTimeUpdate(e) {
    if (time >= duration) {
      ended = true;
      paused = true;
    } else {
      ended = false;
    }
  }

  function revealAIDetails() {
    console.log("TEST SIDEBUTTON");
    showSideAIDetail = !showSideAIDetail;
  }

  function selectVideo(event){
    const video = event.detail;
    console.log("Selected video: ", video);
    videoPath = video;
    extractFrames();
  }

  let sideAIinfo = [
    // {
    //     id: "1",
    //     img: "https://www.ibm.com/blog/wp-content/uploads/2023/03/What-is-Generative-AI-what-are-Foundation-Models-and-why-do-they-matter-1200x630.jpg",
    //     mName: "YoloV8n",
    //     mTime: "06/07/2024",
    // },
    // {
    //     id: "2",
    //     img: "https://www.ibm.com/blog/wp-content/uploads/2023/03/What-is-Generative-AI-what-are-Foundation-Models-and-why-do-they-matter-1200x630.jpg",
    //     mName: "YoloV8n",
    //     mTime: "07/07/2024",
    // },
    // {
    //     id: "3",
    //     img: "https://www.ibm.com/blog/wp-content/uploads/2023/03/What-is-Generative-AI-what-are-Foundation-Models-and-why-do-they-matter-1200x630.jpg",
    //     mName: "YoloV8n",
    //     mTime: "08/07/2024",
    // },
  ];

  async function getAIinfo() {
    try {
      // Fetch video details
      originalVideoPath = get(originalVideoURL);
      appPath = await window.electronAPI.getAppPath();
      const videoName = getFileName(originalVideoPath);
      videoNameExtract = videoName.split(".")[0];

      console.log("Original video path", originalVideoPath);

      const outputDir = `${appPath}/outputVideos/${videoNameExtract}`;

      // Fetch the original video details from the database
      let originalVideo = await window.electronAPI.getVideoByURL(originalVideoPath);

      console.log("Original video", originalVideo);

      // If the original video is not found, add it to the database
      if (!originalVideo) {
        const newOriginalVideo = {
          label: "Original",
          profileImgURL: "https://www.ibm.com/blog/wp-content/uploads/2023/03/What-is-Generative-AI-what-are-Foundation-Models-and-why-do-they-matter-1200x630.jpg",
          videoURL: videoPath,
          originalVidID: 0, // Set to null instead of 0
        };
        originalVideo = await window.electronAPI.addVideo(newOriginalVideo);

        // Fetch the original video again to get the complete data including ID
        originalVideo = await window.electronAPI.getVideoByURL(originalVideoPath);
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
          timeStamp: originalVideo.creation_date,
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
          timeStamp: video.creation_date
        });
      });

      // Format the timestamp
      processedVideos.forEach((video) => {
        video.timeStamp = new Date(video.timeStamp).toLocaleDateString();
      }); 

      // write the processed videos to the sideAIinfo
      processedVideos.forEach((video) => {
        sideAIinfo.push({
          id: video.id,
          img: video.profileImgURL,
          mName: video.label,
          mTime: video.timeStamp,
          mURL: video.videoURL,
        });
      });

      console.log("Get AI info:", sideAIinfo);
    } catch (error) {
      console.error("Error fetching output files:", error);
    }
  }

  function getFileName(filePath) {
    const parts = filePath.split(/[/\\]/);
    return parts[parts.length - 1];
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

<div>
  <div class="flex relative justify-center bg-black overflow-hidden">
    <video
      poster={frames[1]}
      src={videoPath}
      type="video/mp4"
      on:mousemove={handleMove}
      on:touchmove|preventDefault={handleMove}
      on:mousedown={handleMousedown}
      on:mouseup={handleMouseup}
      on:timeupdate={handleTimeUpdate}
      bind:currentTime={time}
      bind:duration
      bind:paused
      bind:volume
    >
      <track kind="captions" />
    </video>
    <div class="sideButton {showSideAIDetail ? 'move-right' : ''}">
      <div class="flex items-center justify-center h-full">
        <Button
          icon
          on:click={revealAIDetails}
          class="text-white"
          size="default"
        >
          {#if !showSideAIDetail}
            <Icon size={50} path={mdiMenuLeftOutline} />
          {:else}
            <Icon size={50} path={mdiMenuRightOutline} />
          {/if}
        </Button>
      </div>
    </div>
    {#if AIinfoDone}
    <div class="sidevideo {showSideAIDetail ? 'move-right' : ''}">
      <div class="m-3">
        {#each sideAIinfo as info}
          <VideoAside AIinfo={info} on:select={selectVideo}/>
        {/each}
      </div>
    </div>
    {/if}
    <div class="controls" style="opacity: {duration && showControls ? 1 : 0}">
      {#if frames.length > 0}
        <div
          on:mouseover={handleMouseEnter}
          on:mouseleave={handleMouseLeave}
          on:focus
          bind:this={thumbnailBar}
          class="thumbnail-bar absolute"
          style="opacity: {showControls ? 1 : 0}"
        >
          {#each frames as frame}
            <div
              class="thumbnail hover:cursor-pointer"
              on:click={() => seekToFrame(frame)}
              on:keypress
            >
              <img src={frame} width="120px" alt={frame} />
            </div>
          {/each}
        </div>
      {/if}
      <div class="w-full flex flex-row justify-start items-center">
        <progress class="TimelineProgress" value={time / duration || 0} />
        <div class="pl-4">
          <button class="w-10 text-white" on:click={pause}>
            {#if ended}
              <Icon size={32} path={mdiReplay} />
            {:else if paused}
              <Icon size={32} path={mdiPlay} />
            {:else}
              <Icon size={32} path={mdiPause} />
            {/if}
          </button>
        </div>
        <div class="info">
          <span class="time">{format(time)}</span>
          <span>:</span>
          <span class="time">{format(duration)}</span>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .sideButton {
    width: 42px;
    height: 42px;
    position: absolute;
    top: 0%;
    right: 0%;
    transition: test 1s;
    background-color: #03191ec6;
    margin: 5px;
    /* border-top-left-radius: 15px; */
    /* border-bottom-left-radius: 15px; */
    border-radius: 50%;
    transition: ease-in-out 1s;
  }

  .sidevideo {
    width: 20%;
    height: fit-content;
    top: 0;
    position: absolute;
    right: -25%;
    margin: 5px;
    background-color: #03191ec6;
    z-index: 10;
    border-radius: 15px;
    transition: ease-in-out 1s;
  }

  .sidevideo.move-right {
    right: 0;
  }

  .sideButton.move-right {
    right: 20.5%;
  }

  ::-webkit-scrollbar {
    width: 10px;
  }

  ::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  /* Handle */
  ::-webkit-scrollbar-thumb {
    background: #888;
  }

  /* Handle on hover */
  ::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

  .thumbnail-bar {
    display: flex;
    overflow-x: hidden;
    overflow-y: hidden;
    width: 100%;
    height: 60px;
    transition: opacity 0.5s;
  }

  .thumbnail {
    flex: 0 0 auto;
    width: 120px;
    height: min-content;
    background-size: cover;
    background-position: center;
    cursor: pointer;
  }

  .thumbnail img {
    opacity: 0.6;
    width: 100%;
    height: 60px;
    object-fit: cover;
  }

  .thumbnail:hover {
    transform: scale(1.1);
    transition: linear 0.2s;
    z-index: 10;
  }

  .thumbnail > img:hover {
    opacity: 1;
  }

  div {
    position: relative;
  }

  .controls {
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    position: absolute;
    bottom: 0;
    gap: 0;
    width: 100%;
    transition: opacity 0.5s;
  }

  .TimelineProgress {
    position: absolute;
    bottom: 40px;
    left: 0;
    width: 100%;
    height: 5px;
  }

  .info {
    display: flex;
    width: fit-content;
    justify-content: center;
  }

  span {
    padding: 0.2em 0.2em;
    color: white;
    text-shadow: 0 0 8px black;
    font-size: 1.4em;
    opacity: 0.7;
  }

  .time {
    width: fit-content;
  }

  progress {
    display: block;
    width: 80%;
    height: 40px;
    position: absolute;
    bottom: 0;
    -webkit-appearance: none;
    appearance: none;
  }

  progress::-webkit-progress-bar {
    background-color: rgb(90, 90, 90);
  }

  progress::-webkit-progress-value {
    background-color: #ff1f1fb2;
  }

  video {
    width: 100%;
    height: 60%;
    aspect-ratio: 16 / 9;
  }
</style>
