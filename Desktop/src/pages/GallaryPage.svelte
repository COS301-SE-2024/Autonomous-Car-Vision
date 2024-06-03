<script>
  import GallaryCard from '../components/GallaryCard.svelte';

  import Sidebar from '../components/Sidebar.svelte';
  import { mdiViewGallery, mdiUpload, mdiCloudPrintOutline } from '@mdi/js';

  const sidebarItems = [
    { name: "Gallery", route: "#/gallary", iconPath: mdiViewGallery },
    { name: "Upload", route: "#/upload", iconPath: mdiUpload },
    { name: "Models", route: "#/models", iconPath: mdiCloudPrintOutline },
  ];

  let videoURLs = [];

  // Fetch the video records from the database
  window.electronAPI.fetchVideos().then(response => {
    if (response.success) {
      videoURLs = response.data.map(record => record.dataValues.localurl);
    } else {
      console.error('Failed to fetch video records:', response.error);
    }
  });
</script>

<div class="w-1/5">
  <Sidebar items={sidebarItems} />
</div>
<div class="items-center w-4/5 ml-auto">
  <div>
    <div class="text-xl font-heading text-theme-keith-accentone text-center rounded">Video Gallery</div>
    <div class="grid grid-flow-row-dense grid-cols-3 items-center">
      {#each videoURLs as url}
        <GallaryCard VideoSource={url}/>
      {/each}
    </div>
  </div>
</div>
