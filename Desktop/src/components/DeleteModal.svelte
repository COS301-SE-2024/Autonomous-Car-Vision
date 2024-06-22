<script>
  import { push } from 'svelte-spa-router';
  import { createEventDispatcher } from "svelte";

  export let videoPath;
  const dispatch = createEventDispatcher();

  function cancel() {
    dispatch("cancel");
  }

  async function deleteVideo() {
    try {
      const response = await window.electronAPI.deleteVideoFile(videoPath);
      if (response.success) {
        console.log(`Deleted file: ${videoPath}`);
        // Handle post-deletion actions, like updating the UI or redirecting
        // For example, you might want to redirect to another page:
        // location.goto("/some-other-page");
        dispatch("deleteVideo");
        push("/gallery");
      } else {
        console.error("Failed to delete file:", response.error);
      }
    } catch (error) {
      console.error("Error deleting file:", error);
    }
  }
</script>

<div
  class="fixed inset-0 flex items-center justify-center bg-theme-dark-background bg-opacity-50 z-50"
>
  <div
    class="bg-white p-6 rounded-lg shadow-lg border border-theme-keith-primary"
  >
    <div class="flex flex-col items-center justify-center">
      <h3 class="text-center">
        Are you sure you would like to delete the video from your downloads?
      </h3>
      <br />
      <p class="text-center">
        You will have to re-download the video from the server to access it in
        future.
      </p>
    </div>

    <div class="flex mt-4 space-x-4">
      <button
        on:click={cancel}
        class="px-4 py-2 bg-theme-dark-primary text-white rounded"
        >Cancel</button
      >
      <button
        on:click={deleteVideo}
        class="px-4 py-2 bg-theme-dark-error text-white rounded">Delete</button
      >
    </div>
  </div>
</div>
