<script>
  import Router from 'svelte-spa-router';
  import routes from './routes/routes';
  import Sidebar from './components/Sidebar.svelte';
  import { mdiViewGallery, mdiUpload, mdiCloudPrintOutline } from '@mdi/js';
  const sidebarItems = [
    { name: "Gallery", route: "#/gallary", iconPath: mdiViewGallery },
    { name: "Upload", route: "#/upload", iconPath: mdiUpload },
    { name: "Models", route: "#/models", iconPath: mdiCloudPrintOutline },
  ];
  const ttoken = localStorage.getItem("token");
  
</script>

<div class="flex">
  {#if ttoken}
  <div class="w-1/5">
    <Sidebar items={sidebarItems} />
  </div>
  {/if}
  <div class="flex-1 items-center p-4">
    <Router {routes} />
  </div>
</div>
