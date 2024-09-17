<script>
  import Router from "svelte-spa-router";
  import routes from "./routes/routes";
  import { cuda, loadState } from "./stores/processing";
  import { theme } from './stores/themeStore.js';


  import toast, { Toaster } from "svelte-french-toast";
  import { onMount } from "svelte";

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
        position: "top-center",
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
  
  let currentTheme;
  $: {
    theme.subscribe(value => {
      currentTheme = value;
    });
  }

  function toggleTheme() {
    if (currentTheme === 'highVizLight') {
      theme.set('highVizDark');
    } else {
      theme.set('highVizLight');
    }
  }

$: {
  theme.subscribe(value => {
    currentTheme = value;
    // Change the body class when the theme changes
    document.body.className = theme === 'theme' ? 'highVizLight' : 'highVizDark';
  });
}
</script>

<div>
  <!-- class="mainContainer" -->
  <Toaster />
  <Router {routes} />
  

</div>

<style>
   @import './global.css';
  /* .mainContainer {
    background-image: linear-gradient(180deg, #001524, #181818);
    width: 100% !important;
  } */
</style>
