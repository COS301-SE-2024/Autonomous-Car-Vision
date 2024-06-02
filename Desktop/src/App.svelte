<script>
  import Router from 'svelte-spa-router';
  import routes from './routes/routes';
  import Sidebar from './components/Sidebar.svelte';

  import { mdiViewGallery } from "@mdi/js";
  import { mdiUpload } from "@mdi/js";
  import { mdiCloudPrintOutline } from "@mdi/js";

  const sidebarItems = [
    { name: "Gallery", route: "#/", iconPath: mdiViewGallery },
    { name: "Upload", route: "#/upload", iconPath: mdiUpload },
    { name: "Models", route: "#/models", iconPath: mdiCloudPrintOutline },
  ];
</script>

<div class="flex">
  <div class="w-1/5">
    <Sidebar items={sidebarItems} />
  </div>
  <div class="flex-1 items-center p-4">
    <Router {routes} />
  </div>
</div>
