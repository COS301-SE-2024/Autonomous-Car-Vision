<script>
    import { writable } from 'svelte/store';
    import EditVideoModal from './EditVideoModal.svelte';
    import DeleteModal from './DeleteModal.svelte';
    import ModelList from './ModelList.svelte';
    import ViewVideoModal from './ViewVideoModal.svelte';
    import { createEventDispatcher } from 'svelte';
    import { push } from 'svelte-spa-router';
  
    const dispatch = createEventDispatcher();
    const currentTab = writable('original');
    const showModelList = writable(false);
    let selectedModel = null;
  
    export let imgSource;
    export let videoSource;
    let modalDefault = "https://placekitten.com/300/300"
    let showEditModal = false;
    let showViewModal = false;
    let showDeleteModal = false;
  
    function back(event) {
        event.stopPropagation(); // Stop event propagation
        dispatch('close');
    }
  
    function switchTab(tab) {
        currentTab.set(tab);
    }
  
    function edit() {
        push('/upload', { videoSource }); // Navigate to /upload with videoSource as a parameter
    }
  
    function process() {
        // Process functionality
    }
  
    function reProcess() {
        // re-process functionality
    }
  
    function deleteItem() {
        showDeleteModal = true;
    }
  
    function model() {
        // Model functionality
    }
  
    function handleCancel() {
        showEditModal = false;
        showDeleteModal = false;
    }
  
    function handleEditSave() {
        // Logic to save the edited video length
        showEditModal = false;
    }
  
    function handleDeleteSave() {
        // Logic to delete the video
        showDeleteModal = false;
    }
  
    function toggleModelList() {
        showModelList.update(value => !value);
    }
  
    function handleModelSelect(event) {
        selectedModel = event.detail;
        showModelList.set(false);
    }
  
    function toggleViewModal() {
        showViewModal = true;
    }
  
    function handleViewDone() {
        showViewModal = false;
    }
  </script>
  
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="fixed inset-0 flex items-center justify-center z-50" on:click|stopPropagation={back}>
      <div class="relative bg-theme-keith-secondary p-8 rounded-lg shadow-lg w-full max-w-2xl border border-theme-keith-primary">
          <div>
              <button class="text-white border-none p-2 rounded cursor-pointer text-xs" on:click={back}>Back</button>
          </div>
          <div class="flex justify-between border-b mb-4">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <div class="py-2 px-4 cursor-pointer { $currentTab === 'original' ? 'border-b-2 font-bold' : '' }" on:click={() => switchTab('original')}>Original</div>
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <div class="py-2 px-4 cursor-pointer { $currentTab === 'processed' ? 'border-b-2 font-bold' : '' }" on:click={() => switchTab('processed')}>Processed</div>
          </div>
  
          <div class="{ $currentTab === 'original' ? 'block' : 'hidden' }">
              <div class="flex flex-col items-center mb-4">
                  <img src={imgSource} alt="video thumbnail" class="w-1/2" />
                  <p class="mt-4">Details here</p>
              </div>
              <div class="flex space-x-4">
                  <button class="text-white p-2 rounded" on:click={edit}>Edit</button>
                  <button class="text-white p-2 rounded" on:click={process}>Process</button>
                  <button class="text-white p-2 rounded" on:click={deleteItem}>Delete</button>
                  {#if showDeleteModal}
                      <DeleteModal on:cancel={handleCancel} on:save={handleDeleteSave} />
                  {/if}
                  <div>
                      <button class="text-white p-2 rounded-full" on:click={toggleModelList}>
                          {#if selectedModel}
                              <img src={selectedModel.profileImg} alt="Selected Model" class="w-10 h-10 rounded-full" />
                          {:else}
                              <img src={modalDefault} alt="default Model" class="w-10 h-10 rounded-full" />
                          {/if}
                      </button>
                      {#if $showModelList}
                          <ModelList on:select={handleModelSelect} />
                      {/if}
                  </div>
              </div>
          </div>
  
          <div class="{ $currentTab === 'processed' ? 'block' : 'hidden' }">
              <div class="flex flex-col items-center mb-4">
                  <img src={imgSource} alt="video thumbnail" class="w-1/2" />
                  <p class="mt-4">Details here</p>
              </div>
              <div class="flex space-x-4">
                  <button class="text-white p-2 rounded" on:click={edit}>View</button>
                  <button class="text-white p-2 rounded" on:click={reProcess}>Re-Process</button>
              </div>
          </div>
      </div>
  </div>