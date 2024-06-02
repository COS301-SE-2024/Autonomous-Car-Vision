<script>
  import Dropzone from "svelte-file-dropzone";

  export let videoSource;

  function handleFilesSelect(e) {
    const { acceptedFiles, fileRejections } = e.detail;
    
    if (acceptedFiles.length > 0) {
      videoSource = URL.createObjectURL(acceptedFiles[0]);
    }

    // Alert for rejected files
    fileRejections.forEach((rejection) => {
      alert(
        `File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`
      );
    });
  }

  function saveVideo() {
    // Add logic to save the video or perform any action on save
    alert('Video saved!');
  }
</script>

<div class="flex flex-col items-center justify-center border-2 border-gray shadow-lg p-6 rounded-lg bg-gray-light max-w-lg mx-auto my-8 relative space-y-5">
  {#if videoSource === ""}
    <Dropzone
      on:drop={handleFilesSelect}
      accept="video/*"
      containerStyles="border-color: #8492a6; color: black"
      multiple={false}
    />
  {:else}
    <video class="video-preview w-full mt-4" src={videoSource} controls>
      <track kind="captions">
    </video>
  {/if}
  <div class="w-full flex items-center mt-4">
    <span class="flex-grow"></span>
    <button class="bg-blue text-white font-bold py-2 px-4 rounded hover:bg-gary-dark" on:click={saveVideo}>Save</button>
  </div>
</div>