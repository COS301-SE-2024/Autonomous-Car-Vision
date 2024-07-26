<script>
  import Router from "svelte-spa-router";
  import routes from "./routes/routes";
  import Sidebar from "./components/Sidebar.svelte";
  import { cuda, loadState } from "./stores/processing";

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

  onMount(async () => {
    window.electronAPI.onPythonScriptDone((event, message) => {
      toast.success(message, {
        duration: 5000,
        position: 'top-center',
      });
    });

    // Listen for state changes from Electron main process
    window.electronAPI.onProcessChanged(async () => {
        await loadState();
    });

    // call cuda-check and console.log
    const isCuda = await window.electronAPI.checkCUDA();
    console.log("Cuda: ", isCuda);
    cuda.set(isCuda);
  });
</script>

<div>
  <Toaster />
  <Router {routes} />
</div>

