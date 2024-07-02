<script>
    import { createEventDispatcher } from 'svelte';
    import { processing, videoUrl } from './stores/processing';
  
    const dispatch = createEventDispatcher();
  
    export let processedVideos = [];

    let processingVideo;
    let currrentVideoUrl;
  
    function selectModel(model) {
      dispatch('select', model);
    }

    // Subscripe to the processing store
    processing.subscribe((value) => {
      processingVideo = value;
    });

    // Subscribe to the videoUrl store
    videoUrl.subscribe((value) => {
      currrentVideoUrl = value;
    });
  </script>
  
  <div class="absolute top-0 right-0 bg-theme-dark-white border border-theme-dark-backgroundBlue g p-4 z-50 flex flex-col rounded-lg">
    {#each processedVideos as video}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="mb-2 cursor-pointer flex items-center rounded border-b border-theme-dark-primary text-black" on:click={() => selectModel(video)}>
        <img src={video.profileImgURL} alt="Model Profile" class="w-12 h-12 rounded-full mr-2">
        <p class="text-xs text-black">{video.label}</p>
      </div>
    {/each}
  </div>