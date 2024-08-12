<script>
  import { push } from "svelte-spa-router";
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

<div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
  <div
    class="bg-theme-dark-background p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
  >
    <div class="flex flex-col boder border-theme-dark-backgroundBlue">
      <p class="text-md">
        Are you sure you would like to delete the video from your downloads?
      </p>
      <div class="flex mt-4 space-x-4">
        <button
          on:click={cancel}
          class="font-medium px-4 py-2 bg-theme-dark-primary text-white rounded"
          >Cancel</button
        >
        <button
          on:click={deleteVideo}
          class="font-medium px-4 py-2 bg-theme-dark-error text-white rounded"
          >Delete</button
        >
      </div>
    </div>
  </div>
</div>
