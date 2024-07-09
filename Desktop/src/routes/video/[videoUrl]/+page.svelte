<script>
  import { location, push } from "svelte-spa-router";

  import { writable, get } from "svelte/store";

  import { VideoURL } from "../../../stores/video";

  import { onMount } from "svelte";

  import {
    processing,
    videoUrl,
    originalVideoURL,
    processingQueue,
    loadState,
  } from "../../../stores/processing";

  import { isLoading } from "../../../stores/loading";
  import QuantamLoader from "../../../components/QuantamLoader.svelte";

  import NestedTimeline from "../../../components/NestedTimeline.svelte";
  import ProtectedRoutes from "../../ProtectedRoutes.svelte";
  import ViewVideoComponent from "../../../components/ViewVideoComponent.svelte";
  import DeleteModal from "../../../components/DeleteModal.svelte";
  import ModelList from "../../../components/ModelList.svelte";

  import ProcessPopup from "../../../components/ProcessPopup.svelte";
  let showProcessPopup = false;

  // TODO: Styling and conditional formatting

  const showModelList = writable(false);

  let appPath = "";
  let scriptPath = "";
  let videoPath;
  let videoName;
  let outputVideoPath;
  let modelName = "yolov8n";
  let modelsPath = "";
  let videoNameExtract = "";
  let extention = "";
  let models = [];
  let selectedModelName = "yolov8n";

  let output = ""; // Store the output of the Python script
  let outputFiles = []; // Store the output files

  function getFileName(filePath) {
    const parts = filePath.split(/[/\\]/);
    return parts[parts.length - 1];
  }

  async function getVideoDetails() {
    return new Promise((resolve) => {
      originalVideoURL.subscribe(async (value) => {
        appPath = await window.electronAPI.getAppPath();
        videoPath = value;
        videoName = await getFileName(videoPath);
        //extract video name from video name without the extention
        videoNameExtract = videoName.split(".")[0];
        extention = videoName.split(".")[1];
        outputVideoPath = `${appPath}/outputVideos/${videoNameExtract}/${videoNameExtract}_processed_${modelName}.${extention}`;
        const appDirectory = await window.electronAPI.resolvePath(
          appPath,
          "..",
        );
        scriptPath = `${appDirectory}/Models/processVideo.py`;
        modelsPath = `${appDirectory}/Models/${modelName}/${modelName}.pt`;
        resolve();
      })();
    });
  }

  async function getOutputFiles() {
    try {
      const outputDir = `${appPath}/outputVideos/${videoNameExtract}`;
      const files = await window.electronAPI.readDirectory(outputDir);

      await loadState();

      // Fetch the original video details from the database
      let originalVideo = await window.electronAPI.getVideoByURL(videoPath);

      console.log("Original video:", originalVideo);

      // If the original video is not found, add it to the database
      if (!originalVideo) {
        const newOriginalVideo = {
          label: "Original",
          profileImgURL: "https://placekitten.com/300/300",
          videoURL: videoPath,
          originalVidID: 0, // Original videos have their originalVidID set to 0 or null
        };
        originalVideo = await window.electronAPI.addVideo(newOriginalVideo);
        console.log("Original video add:", originalVideo);
      }

      // Start with the original video
      outputFiles = [
        {
          id: originalVideo.videoID,
          label: "Original",
          profileImgURL: originalVideo.profileImgURL,
          videoURL: originalVideo.videoURL,
        },
      ];

      // Fetch processed videos linked to the original video
      const processedVideos = await window.electronAPI.getProcessedVideos(
        originalVideo.videoID
      );

      // Add processed videos
      processedVideos.forEach((video) => {
        outputFiles.push({
          id: video.videoID,
          label: video.label,
          profileImgURL: video.profileImgURL,
          videoURL: video.videoURL,
        });
      });

      console.log("Output files:", outputFiles);
    } catch (error) {
      console.error("Error fetching output files:", error);
    }
  }

  async function fetchModels() {
    try {
      const result = await window.electronAPI.getAIModels();
      if (result.success) {
        models = result.data;
        if (models.length > 0) {
          selectedModelName = models[0].model_name;
        }
      } else {
        console.error("Failed to fetch AI models:", result.error);
      }
    } catch (error) {
      console.error("Failed to fetch models", error);
    }
  }

  onMount(async () => {
    await fetchModels();
    await getVideoDetails();
    // await getOutputFiles();
    await loadState(); // Load state on mount

    console.log("Test Video URL page: ", get(videoUrl));

    // if (outputFiles.length > 1) {
    //   showModelList.set(true);
    // }
    console.log($location);
  });

  let processed = false; // Check if the video has been processed

  async function processVideo(event) {
    modelName = event.detail.modelName;
    showProcessPopup = false;
    // isLoading.set(true);
    try {
      await getVideoDetails();

      console.log(isLoading, "isLoading");

      const videoDetails = {
        scriptPath,
        videoPath,
        outputVideoPath,
        modelPath: modelsPath,
      };
    
      setInterval(() => {
        isLoading.set(false);
      }, 15000);
      showModelList.set(true);
    
      await window.electronAPI.queueVideo(videoDetails); // Queue the video for processing

      await loadState(); // Load state after adding the video to the queue

      console.log("Queued video for processing now:", videoDetails);

      // Add processed video information to the database
      const originalVideo = await window.electronAPI.getVideoByURL(videoPath);
      if (originalVideo) {
        const processedVideoURL = outputVideoPath;
        const existingProcessedVideo =
          await window.electronAPI.getVideoByURL(processedVideoURL);

        if (!existingProcessedVideo) {
          const newProcessedVideo = {
            label: modelName,
            profileImgURL:
              "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            videoURL: processedVideoURL,
            originalVidID: originalVideo.videoID,
          };
          await window.electronAPI.addVideo(newProcessedVideo);
        } else {
          console.log(
            "Processed video already exists in the database and will not be added again."
          );
        }
      } else {
        console.error("Original video not found in the database");
      }
    } catch (error) {
      output = error.message;
      console.error("Error:", output);
    }
    console.log("Processing video");
    processed = true;
  }

  function re_process() {
    // Re-process functionality
    console.log("Re-processing video");
  }

  let selectedModel = null;
  let showDeleteModal = false;

  let modalDefault =
    "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";

  function closeProcessPopup() {
    showProcessPopup = false;
  }

  function handleCancel() {
    showDeleteModal = false;
  }

  function handleDeleteSave() {
    // Logic to delete the video
    showDeleteModal = false;
  }

  function deleteItem() {
    showDeleteModal = true;
  }

  function toggleModelList() {
    showModelList.update((value) => !value);
  }

  function handleModelSelect(event) {
    VideoURL.set(event.detail.videoURL);
    selectedModel = event.detail;
    showModelList.set(false);
  }
</script>

<ProtectedRoutes>
  <div class="grid grid-cols-5">
    <div class="col-span-5">
      <!-- {processed ? 'col-span-4' : 'col-span-5'} -->
      <ViewVideoComponent videoPath={$location} />
      <!-- {#if $isLoading}
        <div
          class="flex flex-col justify-center items-center flex-nowrap"
          style="aspect-ratio: 16/9"
        >
          <QuantamLoader />
          
        </div>
      {:else}
        <ViewVideoComponent videoPath={$location} />
      {/if} -->
      <div class="flex space-x-4 align-center p-2 bg-theme-dark-backgroundBlue">
        <button
          class="text-white font-medium p-2 h-10 rounded bg-theme-dark-primary hover:bg-theme-dark-highlight"
          on:click={() => (showProcessPopup = true)}>Process</button
        >
        <button
          class="text-white font-medium p-2 h-10 rounded bg-red hover:bg-red-hover"
          on:click={deleteItem}>Delete</button
        >
        {#if showDeleteModal}
          <DeleteModal
            on:cancel={handleCancel}
            on:save={handleDeleteSave}
            {videoPath}
          />
        {/if}
        <div>
          <!-- <button
            class="text-white p-0.5 rounded-full bg-theme-dark-primary hover:bg-theme-dark-highlight"
            on:click={toggleModelList}
          >
            {#if selectedModel}
              <img
                src={selectedModel.profileImgURL}
                alt="Selected Model"
                class="w-12 h-12 rounded-full"
              />
            {:else}
              <img
                src={modalDefault}
                alt="default Model"
                class="w-12 h-12 rounded-full"
              />
            {/if}
          </button> -->
          <!-- {#if $showModelList}
            <ModelList
              on:select={handleModelSelect}
            />
          {/if} -->
        </div>
      </div>
      {#if showProcessPopup}
        <ProcessPopup
          on:closePopup={closeProcessPopup}
          on:processVideo={processVideo}
          {showProcessPopup}
          {models}
          {selectedModelName}
        />
      {/if}
    </div>

    <!--Put video and editor and buttons-->
    {#if false}
      <div class="col-span-1">
        <NestedTimeline />
        <!--style-->
      </div>
    {/if}
  </div>
</ProtectedRoutes>
