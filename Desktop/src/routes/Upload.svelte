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

  async function saveVideoToServer() {
    let url = "http://localhost:8000/uploadFile/";
    let response = '';
    let error = '';
      const postData = {
        uid: window.electronAPI.getUid(),
        token: "TOKEN",
        aid: "8",
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

  const saveVideo = async () => {
    if (!videoSource) {
      toast.error("Upload a video file to get started", {
        duration: 5000,
        position: "top-center",
      });
      return;
    }
    console.log("TESTING SAVE before try block");

    // isUploadLoading.set(true);
    isUploading = true;
    setInterval(async () => {
      // isUploadLoading.set(true);
      isUploading = false;
      }, 6000);
    

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
    let command = "SEND"

    await window.electronAPI.uploadToAgent(aip, aport, file.path, uid, mid, size, token, command);

    try {
      // Save the file using the main process
      videoSource = await window.electronAPI.saveFile(file.path, filename);
      let record = {
        mname: filename,
        localurl: videoSource,
      };
      // Insert the record into the database
      const response1 = await window.electronAPI.insertData(record);
      console.log("resp1", response1);

      // Select the record from the database
      const response2 = await window.electronAPI.selectData(filename);
      console.log("resp2", response2);

      toast.success("Video uploaded successfully", {
        duration: 5000,
        position: "top-center",
      });


      // sleep for 5 seconds
      await new Promise((resolve) => setTimeout(resolve, 5000));


      console.log("TESTING SAVE before IF");

      if (response2.success) {
        const mid = response2.data.dataValues.mid;
        const uid = window.electronAPI.getUid();
        const token = window.electronAPI.getToken();

        console.log($location);

      } else {
        console.error("Failed to retrieve the record:", response2.error);
      }
      console.log("TESTING SAVE BEFORE PUSHING SUPPOSED TO HAPPEN");

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
            class="bg-theme-dark-backgroundBlue text-theme-dark-white font-bold py-2 px-4 rounded hover:bg-theme-dark-highlight"
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
</ProtectedRoutes>
