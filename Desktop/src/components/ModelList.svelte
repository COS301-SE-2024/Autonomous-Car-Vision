<script>
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
  
    export let processedVideos = [];
  
    function selectModel(model) {
      dispatch('select', model);
    }
  </script>
  
  <div class="absolute top-0 right-0 bg-theme-dark-backgroundBlue border border-gray-300 shadow-lg p-4 z-50 flex flex-col rounded-lg">
    {#each processedVideos as video}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="mb-2 cursor-pointer flex items-center rounded border-b border-theme-dark-primary text-theme-dark-primary" on:click={() => selectModel(video)}>
        <img src={video.profileImgURL} alt="Model Profile" class="w-12 h-12 rounded-full mr-2">
        <p class="text-xs text-theme-dark-primary">{video.label}</p>
      </div>
    {/each}
  </div>