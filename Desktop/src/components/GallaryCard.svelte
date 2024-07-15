<script>
  import { onMount } from "svelte";
  import GallaryMore from "./GallaryMore.svelte";
  import PingLoader from "../components/PingLoader.svelte";
  import { VideoURL } from "../stores/video";
  import { writable } from "svelte/store";
  import { mdiDownload } from "@mdi/js";
  import { Icon } from "svelte-materialify";

  // import { isDownloading } from "../stores/loading";
  import RingLoader from "./RingLoader.svelte";
  import { push } from "svelte-spa-router";
  import axios from "axios";

  export let VideoSource;
  export let VideoName;
  export let isDownloaded;

  let isGalLoading = false;
  let showMoreModal = false;
  let firstFrameURL = "";
  let isDownloading = false;

  async function saveVideoToServer() {
    let url = "http://localhost:8000/uploadFile/";
    let response = '';
    let error = '';
      const postData = {
        uid: window.electronAPI.getUid(),
        token: "TOKEN",
        aid: "1",
        size: "10",
        utoken: "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF1UHc3T255U011V1BreXkwTnJWTApOa0taNzBEU2xWajdpWXVSd1FiTnR4RVFDc2Nrb1BWMzgzaDcyY3lmKzZuZW5MK05WYmpHeGJaMjhoMXgybjl6Cko5ZFRLa1VkaDE2UCsvSlY2VW5oR1lwTmYxY01ubjYzUy9RMWZsVnNxTDVaZ3VpcXRpbHJkZ2ZaRE4yODAwVFcKblVRbXNqQzV5SzJITXBrbHU0bi9ZN2ZTY0ZwYnpGdzJMY1hTVlZaRUZuaWpSY1lXR0ZLS2FPL0JwNGNDV2dkcwpWQ25mcmJDeHM2MGZ5cDR2SzBnWmVpTmEzcXJUaThXN3F3aDNpR2hzYWw1ZmZNOWhQaUJlaXc2bGtQWnYyUTJMCmhFUVhIcVBUMFNtay9BSW1tb1dwVUZCYW9maTd0LzB1L2V4Ylg5MHJpb2kzR1RxMTYzYmd3VnFEMTV4MWQzRHQKeVFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg"
      };

      try {
      const res = await axios.post(url, postData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      response = res.data;
      return response;
    } catch (e) {
      error = e.response ? `Error: ${e.response.status} - ${e.response.statusText}` : 'An error occurred';
      console.error(error);
      throw new Error(error);
    }
  }

  const handleDownload = async (event) => {
    event.stopPropagation();
    // isDownloading.set(true);
    isDownloading = true;

    let response;
    try {
      response = await saveVideoToServer();
    } catch (error) {
      console.error("Failed to save video to server:", error);
      return;
    }

    const { aip, aport } = response;
    console.log(`IP: ${aip}, Port: ${aport}`);

    let uid = window.electronAPI.getUid();
    let mid = "1";
    let size = "10";
    let token = "TOKEN"
    let command = "RETR"

    await window.electronAPI.uploadToAgent(aip, aport, VideoName, uid, mid, size, token, command);

    // move the video to the download folder
    let currentFilePath = VideoName;
    console.log("Current File Path: ", currentFilePath);
    console.log("videoSource: ", VideoSource);

    await window.electronAPI.moveVideo(currentFilePath, VideoName);

    // try {
    //   const response = await window.electronAPI.downloadVideo(
    //     VideoName,
    //     VideoSource
    //   );
    //   console.log(response.success, response.filePath);
    // } catch (error) {}
    // setTimeout(() => {
    //   // isDownloading.set(false);
    // }, 1000);
      isDownloading = false;
      showMoreModal = false;
      isDownloaded = true;

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
    console.log("Video Source Path", VideoSource, "Video Name: ", VideoName);
    if (!isDownloaded) {
      try {
        const response = await window.electronAPI.getVideoFrame(
          VideoSource,
          VideoName
        );
        let videoPaths = response;
        firstFrameURL = videoPaths[0];
        console.log(firstFrameURL);
      } catch (error) {}
    }
    setInterval(() => {
      isGalLoading = false;
    }, 3000);
  });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
  class="{isDownloaded
    ? 'cursor-default'
    : 'notDownloaded'} shadow-card-blue relative overflow-hidden rounded-lg p-2 w-10/12 shadow-md shadow-theme-keith-accenttwo m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
  on:click={goToVideo}
>
  {#if isGalLoading}
    <div class="flex justify-center items-center h-44">
      <div class="flex justify-center">
        <PingLoader />
      </div>
    </div>
  {/if}
  {#if !isGalLoading}
    <div class="image-container relative">
      <!-- style="filter: {!isDownloaded ? 'grayscale(1);' : ''}" add grayscale when notDownloaded current solution doesn't work -->
      <img
        src={firstFrameURL}
        alt="video preview"
        class="h-40 w-full rounded-lg transition-filter duration-300 ease-in-out hover:filter-blur"
      />
      <div
        class="{isDownloaded
          ? 'hover:block'
          : 'hover:hidden'} lg:w-4/12 button-container absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
        style="top:50%; left:50%; transform: translate(-50%, 50%);"
      >
        {#if !isDownloading && !isDownloaded}
          <button
            class="more bg-theme-dark-download text-theme-dark-lightText w-full border-none px-2 py-1 rounded lg:text-md text-sm text-center justify-content-center display-flex align-items-center cursor-pointer"
            on:click={handleDownload}
          >
            <Icon path={mdiDownload} size="24" /></button
          >
        {:else if !isDownloaded}
          <div class="flex justify-center">
            <RingLoader />
          </div>
        {/if}
      </div>
    </div>
    <div class="details p-2">
      <p class="details-link h-12 text-wrap overflow-hidden text-theme-dark-lightText">{VideoName}</p>
    </div>
  {/if}
</div>

{#if showMoreModal && isDownloaded}
  <div>
    <GallaryMore
      imgSource={firstFrameURL}
      videoSource={VideoSource}
      videoName={VideoName}
      on:close={handleBack}
    />
  </div>
{/if}

<style>
  .notDownloaded {
    filter: grayscale(100%);
    cursor: pointer;
    shadow: grayscale;
  }

  .cursor-default {
    cursor: default;
  }
</style>
