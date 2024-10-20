<script>
  import { push } from "svelte-spa-router";
  import { createEventDispatcher } from "svelte";
  import { onMount } from "svelte";
  import { get } from "svelte/store";

  import { cuda, localProcess } from "../stores/processing";

  import { isLoading, isProcessing } from "../stores/loading";
  
  import { theme } from "../stores/themeStore";

  export let showProcessPopup;
  export let models = [];
  export let selectedModelName;

  let localSelcted = "local";

  const dispatch = createEventDispatcher();

  function closePopup() {
    dispatch("closePopup");
  }

  function processVideo() {
    isProcessing.set(true);
    isLoading.set(true);
    dispatch("processVideo", { modelName: selectedModelName });
  }

  function handleModelChange(event) {
    selectedModelName = event.target.value;
  }

  function handleLocalChange(event) {
    let local;
    console.log("LOCAL OR SERVER: ", event.target.value);

    if (event.target.value === "local") {
      local = true;
    } else {
      local = true;
    }
    localProcess.set(local);
  }

  let mounted = false;
  let hasCuda = false;
  onMount(async () => {
    hasCuda = get(cuda);
    mounted = true;
  });
</script>

{#if $theme === "highVizLight"}
  {#if mounted}
    <div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
      <div
        class="bg-highVizLight-accent p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
      >
        <div class="flex flex-col boder border-theme-dark-backgroundBlue">
          <p class="text-md">
            Are you sure you want to process this video? Please select a model
            to process below.
          </p>
          <select
            on:change={handleModelChange}
            bind:value={selectedModelName}
            class="mt-2 p-2 border rounded bg-highVizLight-secondary text-white"
          >
            {#each models as model}
              <option value={model.model_name}>{model.model_name}</option>
            {/each} ▼
          </select>
          {#if hasCuda}
            <select
              style="visibility: hidden"
              on:change={handleLocalChange}
              bind:value={localSelcted}
              class="mt-2 p-2 border rounded bg-highVizLight-secondary text-white"
            >
              <!-- <option value="server">Server</option> -->
              <option value="local">Local</option>
            </select>
          {/if}
          <div class="flex mt-4 space-x-4 justify-start">
            <button
              class="bg-highVizLight-error bg-opacity-70 font-medium text-white px-4 py-2 rounded-full hover:bg-opacity-100 transition-all duration-300 ease-in-out"
              on:click={closePopup}>No</button
            >
            <button
              class="bg-highVizLight-secondary bg-opacity-70 font-medium px-4 py-2 text-white rounded-full hover:bg-opacity-100 transition-all duration-300 ease-in-out"
              on:click={processVideo}>Yes</button
            >
          </div>
        </div>
      </div>
    </div>
  {/if}
{:else if mounted}
  <div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
    <div
      class="bg-theme-dark-background p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
    >
      <div class="flex flex-col boder border-theme-dark-backgroundBlue">
        <p class="text-md text-white">
          Are you sure you want to process this video? Please select a model to
          process below.
        </p>
        <select
          on:change={handleModelChange}
          bind:value={selectedModelName}
          class="mt-2 p-2 border rounded bg-theme-dark-primary text-white"
        >
          {#each models as model}
            <option value={model.model_name}>{model.model_name}</option>
          {/each} ▼
        </select>
        {#if hasCuda}
          <select
            on:change={handleLocalChange}
            bind:value={localSelcted}
            class="mt-2 p-2 border rounded bg-theme-dark-primary text-white"
          >
            <!-- <option value="server">Server</option> -->
            <option value="local">Local</option>
          </select>
        {/if}
        <div class="flex mt-4 space-x-4 justify-start">
          <button
            class="bg-theme-dark-error font-medium text-white px-4 py-2 rounded-full"
            on:click={closePopup}>No</button
          >
          <button
            class="bg-theme-dark-primary font-medium px-4 py-2 text-white rounded-full"
            on:click={processVideo}>Yes</button
          >
        </div>
      </div>
    </div>
  </div>
{/if}
