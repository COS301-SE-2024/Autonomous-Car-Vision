<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import Spinner from "../components/Spinner.svelte";
  import { isLoading } from "../stores/loading";
  import toast, { Toaster } from "svelte-french-toast";
  import { Button } from "svelte-materialify";
  import { onMount } from "svelte";
  import { theme } from "../stores/themeStore"; 

  let pipes = [];
  let selectedPipe = "";
  let laneFollowing = false; 
  let avoidance = false;

  $: textColor = $theme === "highVizLight" ? "black" : "white";

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

    if (laneFollowing) {
      try {
        const appPath = await window.electronAPI.getAppPath();
        const appDirectory = await window.electronAPI.resolvePath(
          appPath,
          ".."
        );
        const scriptPath = `${appDirectory}/HighViz/python-scripts/python/lane_following.py`;

        const exitCode = await window.electronAPI.runPythonScript2(
          scriptPath,
          []
        );

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
    } else if (avoidance) {
      try {
        const appPath = await window.electronAPI.getAppPath();
        const appDirectory = await window.electronAPI.resolvePath(
          appPath,
          ".."
        );
        const scriptPath = `${appDirectory}/HighViz/python-scripts/python/manualUnit3.py`;

        const exitCode = await window.electronAPI.runPythonScript2(
          scriptPath,
          []
        );

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
    } else {
      try {
        const appPath = await window.electronAPI.getAppPath();
        const appDirectory = await window.electronAPI.resolvePath(
          appPath,
          ".."
        );
        const scriptPath = `${appDirectory}/HighViz/python-scripts/python/unit3.py`;

        const exitCode = await window.electronAPI.runPythonScript2(scriptPath, [
          selectedPipe,
        ]);

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
      <p class="text-message" style="color: {textColor};">
        Please start the CARLA server before pressing the button.
      </p>
      <p class="text-message" style="color: {textColor};">
        Note: Build your pipe in the "Pipes" section.
      </p>
      <p class="text-message" style="color: {textColor};">Controls:</p>
      <p class="text-message" style="color: {textColor};">
        W,A,S,D-To move the car
      </p>
      <p class="text-message" style="color: {textColor};">
        O to toggle object detection
      </p>
      <p class="text-message" style="color: {textColor};">
        Q to toggle lane following
      </p>

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

      <select
      bind:value={selectedPipe}
      class="styled-dropdown"
      style="color: {textColor};"
      disabled={laneFollowing}
    >
      {#each pipes as pipe}
        <option value={pipe.pipe} style="color: {textColor};"
          >{pipe.pipe}</option
        >
      {/each}
    </select>

      <div class="lane-following-toggle">
        <input
          type="checkbox"
          bind:checked={laneFollowing}
          id="lane-following"
        />
        <label for="lane-following" style="color: {textColor};"
          >Enable Lane Following</label
        >
      </div>

      <div class="avoidance-toggle">
        <input type="checkbox" bind:checked={avoidance} id="avoidance" />
        <label for="avoidance" style="color: {textColor};"
          >Enable Avoidance</label
        >
      </div>
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
    background-color: #007bff;
    background-repeat: no-repeat;
    background-position: right 15px top 50%;
    background-size: 12px 12px;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    outline: none;
    color: inherit;
  }

  .styled-dropdown:focus {
    border-color: #ccc;
  }

  .lane-following-toggle,
  .avoidance-toggle {
    margin-top: 20px;
    display: flex;
    align-items: center;
  }

  .lane-following-toggle input,
  .avoidance-toggle input {
    margin-right: 10px;
  }
</style>
