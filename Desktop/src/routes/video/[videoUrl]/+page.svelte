<script>
  import { location } from "svelte-spa-router";

  import { writable } from "svelte/store";

  import NestedTimeline from "../../../components/NestedTimeline.svelte";
  import ProtectedRoutes from "../../ProtectedRoutes.svelte";
  import ViewVideoComponent from "../../../components/ViewVideoComponent.svelte";
  import DeleteModal from "../../../components/DeleteModal.svelte";
  import ModelList from "../../../components/ModelList.svelte";

  import ProcessPopup from "../../../components/ProcessPopup.svelte";
  let showProcessPopup = false;

  // TODO: Styling and conditional formatting

  const showModelList = writable(false);

  let processed = false; // Check if the video has been processed

  function process() {
    processed = true;
    console.log("Processing video", showProcessPopup);
  }

  function re_process() {
    // Re-process functionality
    console.log("Re-processing video");
  }

  let selectedModel = null;
  let showEditModal = false;
  let showDeleteModal = false;

  let modalDefault =
    "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";

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
  <div class="grid grid-cols-5">
    <div class="{processed ? 'col-span-4' : 'col-span-5'} ">
      <ViewVideoComponent videoPath={$location} />
      <div class="flex space-x-4 align-center p-2 bg-black">
        <button
          class="text-white p-2 h-10 rounded bg-theme-keith-primary hover:bg-theme-green-primary"
          on:click={() => (showProcessPopup = true)}>Process</button
        >
        <button
          class="text-white p-2 h-10 rounded bg-theme-keith-primary hover:bg-theme-green-primary"
          on:click={deleteItem}>Delete</button
        >
        {#if showDeleteModal}
          <DeleteModal on:cancel={handleCancel} on:save={handleDeleteSave} />
        {/if}
        <div>
          <button
            class="text-white p-0.5 rounded-full bg-theme-keith-primary hover:bg-theme-green-primary"
            on:click={toggleModelList}
          >
            {#if selectedModel}
              <img
                src={selectedModel.profileImg}
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
            <ModelList on:select={handleModelSelect} />
          {/if}
        </div>
      </div>
      <ProcessPopup bind:showProcessPopup>
        <div slot="body">
          <h1>Are you sure you want to process this video?</h1>
          <button class="bg-black text-white rounded-xl w-20" on:click={process}>Yes</button>
          <button class="bg-red text-white rounded-xl w-20" on:click={() => (showProcessPopup = false)}>No</button>
        </div>
      </ProcessPopup>
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
