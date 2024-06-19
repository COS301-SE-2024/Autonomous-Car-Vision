<script>
  import { writable } from "svelte/store";

  import NestedTimeline from "./../components/NestedTimeline.svelte";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ViewVideoComponent from "../components/ViewVideoComponent.svelte";
  import DeleteModal from "../components/DeleteModal.svelte";
  import ModelList from "../components/ModelList.svelte";

  // TODO: Styling and conditional formatting


  export const videoURL = "";

  const showModelList = writable(false);

  let processed = true; // Check if the video has been processed

  function process() {
    // Process functionality
    console.log("Processing video");
  }

  function re_process() {
    // Re-process functionality
    console.log("Re-processing video");
  }

  let selectedModel = null;
  let showEditModal = false;
  let showDeleteModal = false;

  let modalDefault = "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";

  function handleCancel() {
    showEditModal = false;
    showDeleteModal = false;
  }

  function deleteItem() {
    showDeleteModal = true;
  }

  function handleDeleteSave() {
    // Logic to delete the video
    showDeleteModal = false;
  }

  function toggleModelList() {
    showModelList.update((value) => !value);
  }

  function handleModelSelect(event) {
    selectedModel = event.detail;
    showModelList.set(false);
  }
</script>

<ProtectedRoutes>
  <div class="grid grid-cols-5 gap-2">
    <div class="col-span-4">
      <ViewVideoComponent videoPath={videoURL} />
    </div>

    <!--Put video and editor and buttons-->
    {#if processed}
      <div class="col-span-1">
        <NestedTimeline />
        <!--style-->
      </div>
    {/if}
  </div>
  <div class="flex space-x-4 align-center pt-2">
    <button class="text-theme-light p-2 h-10 rounded bg-theme-keith-primary" on:click={process}>Process</button>
    <button class="text-theme-light p-2 h-10 rounded bg-theme-keith-primary" on:click={deleteItem}>Delete</button>
    {#if showDeleteModal}
      <DeleteModal on:cancel={handleCancel} on:save={handleDeleteSave} />
    {/if}
    <div>
      <button class="text-theme-light p-1 rounded-full bg-theme-keith-primary" on:click={toggleModelList}>
        {#if selectedModel}
          <img
            src={selectedModel.profileImg}
            alt="Selected Model"
            class="w-10 h-10 rounded-full"
          />
        {:else}
          <img
            src={modalDefault}
            alt="default Model"
            class="w-10 h-10 rounded-full"
          />
        {/if}
      </button>
      {#if $showModelList}
        <ModelList on:select={handleModelSelect} />
      {/if}
    </div>
  </div>
</ProtectedRoutes>
