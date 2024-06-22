<script>
  import { location, push } from "svelte-spa-router";

  import { writable } from "svelte/store";

  import { VideoURL } from "../../../stores/video";
  import { OriginalVideoURL } from "../../../stores/video";

  import { onMount } from "svelte";

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
  let modelName = "yolov8n"
  let modelsPath = "";
  let videoNameExtract = '';
  let extention = '';

  let output = ""; // Store the output of the Python script
  let outputFiles = []; // Store the output files

  function getFileName(filePath) {
    const parts = filePath.split(/[/\\]/);
    return parts[parts.length - 1];
  }

  async function getVideoDetails() {
    return new Promise((resolve) => {
      VideoURL.subscribe(async (value) => {
        
        appPath = await window.electronAPI.getAppPath();
        videoPath = value;
        videoName = await getFileName(videoPath);
        //extract video name from video name without the extention
        videoNameExtract = videoName.split(".")[0];
        extention = videoName.split(".")[1];
        outputVideoPath = `${appPath}/outputVideos/${videoNameExtract}/${videoNameExtract}_processed_${modelName}.${extention}`;
        const appDirectory = await window.electronAPI.resolvePath(appPath, '..');
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

    // Start with the original video
    outputFiles = [{
      id: 0,
      label: "Original",
      profileImgURL: "https://placekitten.com/300/300",
      videoURL: videoPath
    }];

    // Add processed videos
    const processedFiles = files.map((file, index) => {
      // Extract the model name from the file name (assuming the model name is part of the file name)
      const modelNameMatch = file.match(/_processed_(\w+)\./);
      const modelName = modelNameMatch ? modelNameMatch[1] : "unknown";

      return {
        id: index + 1,
        label: modelName,
        profileImgURL: "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        videoURL: `${outputDir}/${file}`
      };
    });

    // Combine original and processed videos
    outputFiles = outputFiles.concat(processedFiles);

    console.log("Output files:", outputFiles);
  } catch (error) {
    console.error("Error reading output directory:", error);
  }
}

  onMount(async () => {
    await getVideoDetails();
    await getOutputFiles();

    if (outputFiles.length > 1) {
      showModelList.set(true);
    }
  });

  let processed = false; // Check if the video has been processed

  async function processVideo() {
    showProcessPopup = false;
    try {
      await getVideoDetails();

      OriginalVideoURL.set(videoPath);

      output = await window.electronAPI.runPythonScript(scriptPath, [
        videoPath,
        outputVideoPath,
        modelsPath,
      ]);
      console.log("Python Script Output:", output);
    } catch (error) {
      output = error.message;
      console.error("Python Script Error:", output);
    }
    processed = true;
    console.log("Processing video");
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
    <div class="{processed ? 'col-span-4' : 'col-span-5'} ">
      <ViewVideoComponent videoPath={$location} />
      <div class="flex space-x-4 align-center p-2 bg-theme-dark-backgroundBlue">
        <button
          class="text-white p-2 h-10 rounded bg-theme-dark-primary hover:bg-theme-dark-highlight"
          on:click={() => (showProcessPopup = true)}>Process</button
        >
        <button
          class="text-white p-2 h-10 rounded bg-theme-dark-primary hover:bg-theme-dark-highlight"
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
          <button
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
          </button>
          {#if $showModelList}
            <ModelList on:select={handleModelSelect} processedVideos={outputFiles}/>
          {/if}
        </div>
      </div>
      {#if showProcessPopup}
        <ProcessPopup
        on:closePopup={closeProcessPopup}
        on:processVideo={processVideo}
        showProcessPopup={showProcessPopup}/>
      {/if}
    </div>

    <!--Put video and editor and buttons-->
    {#if processed}
      <div class="col-span-1">
        <NestedTimeline />
        <!--style-->
      </div>
    {/if}
  </div>
</ProtectedRoutes>
