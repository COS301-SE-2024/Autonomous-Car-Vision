<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import Spinner from "../components/Spinner.svelte";
  import { isLoading } from "../stores/loading";
  import toast, { Toaster } from "svelte-french-toast";
  import { Button } from "svelte-materialify";
  import { onMount } from "svelte";
  import { theme } from '../stores/themeStore'; // Importing the theme store
  
  let pipes = [];
  let selectedPipe = "";

  // Reactive statement to determine text color based on theme
  $: textColor = $theme === 'highVizLight' ? 'black' : 'white';

  async function loadPipes() {
    try {
      const response = await window.electronAPI.getPipeJson();
      if (response.success && response.data.length > 0) {
        pipes = response.data;
        selectedPipe = pipes[0].pipe;
      } else {
        pipes = ["Please create pipes"];
        selectedPipe = pipes[0];
      }
    } catch (error) {
      console.error("Error fetching pipes:", error);
      pipes = [{ pipe: "Please create pipes" }];
      selectedPipe = pipes[0];
    }
  }

  onMount(() => {
    loadPipes();
  });

  async function startCarla() {
    isLoading.set(true);
  
    try {
      const appPath = await window.electronAPI.getAppPath();
      const appDirectory = await window.electronAPI.resolvePath(appPath, "..");
      const scriptPath = `${appDirectory}/Process/pipe4/temp/unit3.py`;
  
      // Pass the selected pipe as an argument to the Python script
      const exitCode = await window.electronAPI.runPythonScript2(scriptPath, [selectedPipe]);
  
      isLoading.set(false);
  
      if (exitCode === 0) {
        toast.success("CARLA ran successfully!", {
          duration: 5000,
          position: "top-center",
        });
      } else {
        toast.error("Please check CARLA server!", {
          duration: 5000,
          position: "top-center",
        });
      }
    } catch (error) {
      isLoading.set(false);
      console.error("Error running CARLA:", error);
    } finally {
      isLoading.set(false);
    }
  }
</script>

<ProtectedRoutes>
  {#if $isLoading}
    <div class="flex justify-center">
      <Spinner />
    </div>
  {:else}
    <Toaster />
    <div class="center-content">
      <!-- Apply text color dynamically based on theme -->
      <p class="text-message" style="color: {textColor};">
        Please start the CARLA server before pressing the button.
      </p>
      <p class="text-message" style="color: {textColor};">
        Note: Build your pipe in the "Pipes" section.
      </p>

      <!-- Button with dynamic text color -->
      <Button
        rounded
        class="bg-dark-primary styled-button"
        style="color: {textColor};"
        on:click={startCarla}
      >
        Start CARLA
      </Button>

      <p class="select-message" style="color: {textColor};">
        Please select a pipe below:
      </p>

      <!-- Styled Dropdown with dynamic text color -->
      <select bind:value={selectedPipe} class="styled-dropdown" style="color: {textColor};">
        {#each pipes as pipe}
          <option value={pipe.pipe} style="color: {textColor};">{pipe.pipe}</option>
        {/each}
      </select>
    </div>
  {/if}
</ProtectedRoutes>

<style>
  .center-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  .text-message {
    font-size: 1.2em;
    margin-bottom: 20px;
    text-align: center;
  }

  .select-message {
    font-size: 1.2em;
    margin-top: 20px;
    text-align: center;
  }

  .styled-dropdown {
    margin-top: 5px;
    padding: 10px;
    font-size: 1.2em;
    border: 2px solid #ccc;
    border-radius: 5px;
    background-color: #007BFF; /* Blue background */
    background-repeat: no-repeat;
    background-position: right 15px top 50%;
    background-size: 12px 12px;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    outline: none;
    color: inherit; /* Inherit text color based on dynamic style */
  }

  .styled-dropdown:focus {
    border-color: #ccc;
  }

  /* Dynamic styling for the button */
  .styled-button {
    margin-top: 10px;
    color: inherit; /* Inherit text color based on dynamic style */
  }
</style>
