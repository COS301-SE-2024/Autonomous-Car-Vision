<script>
  import Dropzone from "svelte-file-dropzone";
  import { push, location } from "svelte-spa-router";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import toast, { Toaster } from "svelte-french-toast";
  import { onMount } from "svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  import { isUploadLoading } from "../stores/uploadLoading";
  import RingLoader from "../components/RingLoader.svelte";
  import axios from "axios";
  import {theme} from '../stores/themeStore';

  export let videoSource = "";
  let filename = "";
  let file;

  let isUploading = false;

  // For loading screen purposes
  onMount(() => {
    // isLoading.set(true);
    // setTimeout(() => {
    //   isLoading.set(false);
    // }, 1000);
  });

  function handleFilesSelect(e) {
    const { acceptedFiles, fileRejections } = e.detail;

    if (acceptedFiles.length > 0) {
      videoSource = URL.createObjectURL(acceptedFiles[0]);
      filename = acceptedFiles[0].name;
      file = acceptedFiles[0];
    }

    // Alert for rejected files
    fileRejections.forEach((rejection) => {
      alert(
        `File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`,
      );
    });
  }

  const saveVideo = async () => {
    if (!videoSource) {
      toast.error("Upload a video file to get started", {
        duration: 5000,
        position: "top-center",
      });
      return;
    }

    // isUploadLoading.set(true);
    isUploading = true;
    setInterval(async () => {
      // isUploadLoading.set(true);
      isUploading = false;
      }, 6000);
    
    let uid = window.electronAPI.getUid();
    let token = window.electronAPI.getToken();
    // let size = "10";
    // let size = window.electronAPI.getFileSize(file.path);
    let sizeInBytes = file.size;
  
  // Convert size to MB and round to 2 decimal places
  let size = (sizeInBytes / (1024 * 1024)).toFixed(2);
    let aip = "";
    let aport = "";
    let command = "SEND";
    try {
    let response = await window.electronAPI.openFTP(uid, token, size, filename, file.path, command);
    
    if (response.success) {
        aip = response.ip;
        aport = response.port;
        // You can now use response.ip and response.port as needed
      } else {
          console.error("Error:", response.error);
      }
    } catch (error) {
        console.error("Error calling openFTP:", error);
    }

    try{
      let testVar = await window.electronAPI.uploadToAgent(aip, aport, file.path, uid, size, token, filename);
    }catch(error){
      console.error("BIG BAD ERROR OHHHH NO", error);
    }

    try {
      // Save the file using the main process
      videoSource = await window.electronAPI.saveFile(file.path, filename);
      let record = {
        mname: filename,
        localurl: videoSource,
      };
      // Insert the record into the database
      const response1 = await window.electronAPI.insertData(record);

      // Select the record from the database
      const response2 = await window.electronAPI.selectData(filename);

      toast.success("Video uploaded successfully", {
        duration: 5000,
        position: "top-center",
      });


      // sleep for 5 seconds
      await new Promise((resolve) => setTimeout(resolve, 5000));



      if (response2.success) {
        const mid = response2.data.dataValues.mid;
        const uid = window.electronAPI.getUid();
        const token = window.electronAPI.getToken();


      } else {
        console.error("Failed to retrieve the record:", response2.error);
      }

      // push("/gallery");
    } catch (error) {
      console.error("Error occurred:", error);
    }
  };
</script>

<ProtectedRoutes>
  {#if $isLoading}
    <div class="flex justify-center">
      <Spinner />
    </div>
  {:else}
    <Toaster />
    {#if $theme === 'highVizLight'}
    <div class="flex justify-center items-center h-screen">
      <div
        class="flex flex-col items-center justify-center border-2 border-gray shadow-lg p-6 rounded-lg bg-gray-light max-w-lg mx-auto my-8 relative space-y-5 h-fit"
      >
        {#if videoSource}
          <video class="video-preview w-full mt-4" src={videoSource} controls>
            <track kind="captions" />
          </video>
        {:else}
          <Dropzone
            on:drop={handleFilesSelect}
            accept="video/*"
            containerStyles="border-color: #8492a6; color: black"
            multiple={false}
          />
        {/if}
        <div class="w-full flex items-center mt-4">
          <span class="flex-grow"></span>
          <button
            class="bg-highVizLight-primary bg-opacity-70  text-theme-dark-white font-bold py-2 px-4 rounded hover:bg-theme-dark-highlight"
            on:click={saveVideo}
            >Save
          </button>
        </div>
        {#if isUploading}
          <div class="flex justify-center">
            <RingLoader />
          </div>
        {/if}
      </div>
    </div>
    {:else}
    <div class="flex justify-center items-center h-screen">
      <div
        class="flex flex-col items-center justify-center border-2 border-gray shadow-lg p-6 rounded-lg bg-gray-light max-w-lg mx-auto my-8 relative space-y-5 h-fit"
      >
        {#if videoSource}
          <video class="video-preview w-full mt-4" src={videoSource} controls>
            <track kind="captions" />
          </video>
        {:else}
          <Dropzone
            on:drop={handleFilesSelect}
            accept="video/*"
            containerStyles="border-color: #8492a6; color: black"
            multiple={false}
          />
        {/if}
        <div class="w-full flex items-center mt-4">
          <span class="flex-grow"></span>
          <button
            class="bg-theme-highVizDark-background  text-theme-dark-white font-bold py-2 px-4 rounded hover:bg-theme-dark-highlight"
            on:click={saveVideo}
            >Save
          </button>
        </div>
        {#if isUploading}
          <div class="flex justify-center">
            <RingLoader />
          </div>
        {/if}
      </div>
    </div>
    {/if}
    

    
  {/if}
</ProtectedRoutes>
