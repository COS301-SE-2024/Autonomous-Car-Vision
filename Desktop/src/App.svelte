<script>
  import Router from "svelte-spa-router";
  import routes from "./routes/routes";
  import Sidebar from "./components/Sidebar.svelte";

  import toast, { Toaster } from 'svelte-french-toast';
  import { onMount } from 'svelte';

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

  onMount(() => {
    window.electronAPI.onPythonScriptDone((event, message) => {
      toast.success(message, {
        duration: 5000,
        position: 'top-center',
      });
    });
  });
</script>

<div>
  <Toaster />
  <Router {routes} />
</div>
