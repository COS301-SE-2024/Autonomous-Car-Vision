<script>
  import Router from 'svelte-spa-router';
  import routes from './routes/routes';
  import Sidebar from './components/Sidebar.svelte';

  import { mdiViewGallery, mdiUpload, mdiCloudPrintOutline } from '@mdi/js';

  const sidebarItems = [
    { name: "Gallery", route: "#/gallery", iconPath: mdiViewGallery },
    { name: "Upload", route: "#/upload", iconPath: mdiUpload },
    { name: "Models", route: "#/models", iconPath: mdiCloudPrintOutline },
  ];


</script>

<div class="w-full flex">
  <div class='w-1/5'>
    <Sidebar items={sidebarItems} />
  </div>
  <div class='w-4/5'>
    <Router {routes} />
  </div>
</div>
