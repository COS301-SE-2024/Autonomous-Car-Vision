<script>
  import Dropzone from "svelte-file-dropzone";
  import { push } from "svelte-spa-router";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import toast, { Toaster } from "svelte-french-toast";
  import { onMount } from "svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  export let videoSource = "";
  let filename = "";
  let file;

  // For loading screen purposes
  onMount(() => {
    isLoading.set(true);
    setTimeout(() => {
      isLoading.set(false);
    }, 1500);
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
        `File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`
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

    let record = {
      mname: filename,
      localurl: videoSource,
    };

    try {
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

      // sleep for 1 second
      await new Promise((resolve) => setTimeout(resolve, 1000));

      if (response2.success) {
        const mid = response2.data.dataValues.mid;
        const uid = window.electronAPI.getUid();
        const token = window.electronAPI.getToken();

        push("/gallery");
      } else {
        console.error("Failed to retrieve the record:", response2.error);
      }
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
    <div
      class="flex flex-col items-center justify-center border-2 border-gray shadow-lg p-6 rounded-lg bg-gray-light max-w-lg mx-auto my-8 relative space-y-5"
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
          class="bg-theme-keith-accentone text-white font-bold py-2 px-4 rounded hover:bg-theme-keith-accenttwo"
          on:click={saveVideo}
          >Save
        </button>
      </div>
    </div>
  {/if}
</ProtectedRoutes>
