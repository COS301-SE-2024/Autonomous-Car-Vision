<script>
    import GallaryCard from '.././components/GallaryCard.svelte';

    let videoURLs = ["https://sveltejs.github.io/assets/caminandes-llamigos.mp4"]

    
  </script>
  
  <div class="max-w-fit mx-autorounded-xl shadow-lg flex items-center space-x-4 ">
    <div>
      <div class="text-xl font-heading text-black">Video Gallary</div>
      <div class="grid grid-flow-row-dense grid-cols-2 space-x-2"> 
      {#each videoURLs as url}
        <GallaryCard VideoSource={url}/>
      {/each}
    </div>
    </div>
  </div>
  