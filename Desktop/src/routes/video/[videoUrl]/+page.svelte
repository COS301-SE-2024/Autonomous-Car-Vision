<script>
  import { location, push } from "svelte-spa-router";

  import { writable, get } from "svelte/store";

  import { VideoURL } from "../../../stores/video";
  import { OriginalVideoURL } from "../../../stores/video";
  import { mdiAccessPoint, mdiDeleteOutline } from "@mdi/js";
  import { Icon } from "svelte-materialify";
  import { isProcessing } from "../../../stores/loading";

  import { onMount } from "svelte";

  import toast, { Toaster } from "svelte-french-toast";

  import {
    processing,
    videoUrl,
    localProcess,
    originalVideoURL,
    processingQueue,
    loadState,
  } from "../../../stores/processing";

  import { isLoading } from "../../../stores/loading";

  import ProtectedRoutes from "../../ProtectedRoutes.svelte";
  import ViewVideoComponent from "../../../components/ViewVideoComponent.svelte";
  import DeleteModal from "../../../components/DeleteModal.svelte";

  import ProcessPopup from "../../../components/ProcessPopup.svelte";
  import { DotLottieSvelte } from "@lottiefiles/dotlottie-svelte";
  let showProcessPopup = false;

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
  let dotLottieProcess;

  let output = "";
  let outputFiles = [];

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
        videoNameExtract = videoName.split(".")[0];
        extention = videoName.split(".")[1];
        outputVideoPath = `${appPath}/outputVideos/${videoNameExtract}/${videoNameExtract}_processed_${modelName}.${extention}`;

        const appDirectory = await window.electronAPI.resolvePath(
          appPath,
          "..",
        );

        await window.electronAPI.resolvePath(
          `${appPath}/outputVideos/${videoNameExtract}/${videoNameExtract}_processed_${modelName}.${extention}`,
          "..",
        )

        scriptPath = `${appDirectory}/HVstore/python-scripts/python/processVideo.py`;

        // modelsDirectory = await window.electronAPI.getModelsPath();
        // modelsPath = `${modelsDirectory}/${modelName}/${modelName}.pt`;
        modelsPath = `${appDirectory}/HVstore/python-scripts/python/models/${modelName}/${modelName}.pt`;
        resolve();
      })();
    });
  }

  async function getOutputFiles() {
    try {
      const outputDir = `${appPath}/outputVideos/${videoNameExtract}`;
      const files = await window.electronAPI.readDirectory(outputDir);

      await loadState();

      let originalVideo = await window.electronAPI.getVideoByURL(videoPath);

      if (!originalVideo) {
        const newOriginalVideo = {
          label: "Original",
          profileImgURL: "https://placekitten.com/300/300",
          videoURL: videoPath,
          originalVidID: 0,
        };
        originalVideo = await window.electronAPI.addVideo(newOriginalVideo);
      }

      outputFiles = [
        {
          id: originalVideo.videoID,
          label: "Original",
          profileImgURL: originalVideo.profileImgURL,
          videoURL: originalVideo.videoURL,
        },
      ];

      const processedVideos = await window.electronAPI.getProcessedVideos(
        originalVideo.videoID,
      );

      processedVideos.forEach((video) => {
        outputFiles.push({
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

  function playLottie(lottie) {
    lottie?.play();
  }

  function pauseLottie(lottie) {
    lottie?.pause();
  }

  onMount(async () => {
    await fetchModels();
    await getVideoDetails();
    await loadState();
    lottieElement1.addEventListener("mouseenter", () =>
      playLottie(dotLottieProcess),
    );
    lottieElement1.addEventListener("mouseleave", () =>
      pauseLottie(dotLottieProcess),
    );
    return () => {
      lottieElement1.removeEventListener("mouseenter", () =>
        playLottie(dotLottieProcess),
      );
      lottieElement1.removeEventListener("mouseleave", () =>
        pauseLottie(dotLottieProcess),
      );
      pauseLottie(dotLottieProcess);
    };
  });

  let processed = false;

  async function processVideo(event) {
    isProcessing.set(true);
    modelName = event.detail.modelName;
    showProcessPopup = false;
    try {
      await getVideoDetails();

      const videoDetails = {
        scriptPath,
        videoPath,
        outputVideoPath,
        modelPath: modelsPath,
        localProcess: true,
      };

      setInterval(() => {
        isLoading.set(false);
      }, 1000);
      showModelList.set(true);

      await window.electronAPI.queueVideo(videoDetails);

      toast.success("Video queued for processing", {
        duration: 5000,
        position: "top-center",
      });

      await loadState();

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
            "Processed video already exists in the database, video will be reprocessed.",
          );
        }
      } else {
        console.error("Original video not found in the database");
      }
    } catch (error) {
      output = error.message;
      console.error("Error:", output);
    }
    processed = true;
    setInterval(() => {
      isProcessing.set(false);
      isLoading.set(false);
    }, 1000);
    showModelList.set(true);
  }

  function re_process() {
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
  <Toaster />
  <div class="grid grid-cols-5 h-full">
    <div class="col-span-5 h-11/12">
      <ViewVideoComponent videoPath={$location} />
      <div class="flex space-x-4 align-center p-2">
        <button
          class="text-white font-medium p-2 w-28 rounded-full bg-theme-dark-primary hover:bg-theme-dark-highlight"
          on:click={() => (showProcessPopup = true)}
        >
          <Icon path={mdiAccessPoint} size={28} />
          Process
        </button>
        <button
          class="text-white font-medium p-2 w-28 rounded-full bg-red hover:bg-red-hover"
          on:click={deleteItem}
        >
          <Icon path={mdiDeleteOutline} size={28} />
          Delete
        </button>
      </div>
      {#if showDeleteModal}
        <DeleteModal
          on:cancel={handleCancel}
          on:save={handleDeleteSave}
          {videoPath}
        />
      {/if}
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
  </div>
</ProtectedRoutes>
