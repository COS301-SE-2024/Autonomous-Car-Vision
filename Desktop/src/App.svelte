<script>
  import Router from "svelte-spa-router";
  import routes from "./routes/routes";
  import Sidebar from "./components/Sidebar.svelte";
  import { mdiViewGallery, mdiUpload, mdiCloudPrintOutline } from "@mdi/js";
  const sidebarItems = [
    { name: "Gallery", route: "#/gallary", iconPath: mdiViewGallery },
    { name: "Upload", route: "#/upload", iconPath: mdiUpload },
    { name: "Models", route: "#/models", iconPath: mdiCloudPrintOutline },
  ];

  window.electronAPI.getToken();
  let ttoken;
  if (window.electronAPI.getToken() != "") {
    ttoken = window.electronAPI.getToken();
  }

  console.log(window.electronAPI.getToken());
</script>

<div class=bg-theme-dark-background>
  <Sidebar {sidebarItems} />
  <Router {routes} />
</div>
