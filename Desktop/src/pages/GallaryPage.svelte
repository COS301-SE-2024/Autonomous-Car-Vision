<script>
    import GallaryCard from '.././components/GallaryCard.svelte';

    let videoURLs = ["https://sveltejs.github.io/assets/caminandes-llamigos.mp4", "https://sveltejs.github.io/assets/caminandes-llamigos.mp4","https://sveltejs.github.io/assets/caminandes-llamigos.mp4"]

    
  </script>
  
  <div class="items-center w-full">
    <div>
      <div class="text-xl font-heading text-theme-keith-accentone text-center rounded">Video Gallary</div>
      <div class="grid grid-flow-row-dense grid-cols-3 items-center"> 
      {#each videoURLs as url}
        <GallaryCard VideoSource={url}/>
      {/each}
    </div>
    </div>
  </div>
  