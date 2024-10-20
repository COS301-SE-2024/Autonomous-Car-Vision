<script>
    import { Button, Icon } from "svelte-materialify";
    import { selectedModel } from "../stores/modelsStore.js"
    import { get } from "svelte/store";
   import {mdiArrowLeftBold} from "@mdi/js";
   import { push } from "svelte-spa-router";
   import {theme} from '../stores/themeStore';
    
    export let Model= get(selectedModel);

    const goBack= () => {
      selectedModel.set(null);
      push("/models");
    };
</script>


{#if $theme === 'highVizLight'}
<div class="bg-highVizLight-secondary rounded-lg">
  <button
        class="text-black border-none p-1 rounded cursor-pointer text-xs bg-highVizLight-secondary hover:bg-theme-dark-background transition-all duration-300 ease-in-out"
        on:click={goBack}> 
          <Icon path={mdiArrowLeftBold} />
        <span class="ml-2"> Back </span>
        </button>
  <div class="grid grid-cols-2 grid-rows-3 bg-highVizLight-secondary grid-rows-2 gap-2 p-4 shadow-lg w-full h-full">
    <div class="relative bg-highVizLight-accent rounded-lg block items-center justify-center col-span-1 row-span-2">
      <video src="https://www.pexels.com/download/video/3121459/" class="p-1 rounded-lg" loop autoplay muted playsinline></video>
      <!-- svelte-ignore a11y-img-redundant-alt -->
    </div>
    
    <div class="flex flex-col p-4 col-span-1 row-span-1">
      <div class="text-2xl  text-primary font-bold justify-center ">{Model.mName}</div>
      <div class=" text-black text-base">{Model.mDescription}</div>
      <div class="align-right font-bold text-black justify-right mt-2 text-lg "> Version: {Model.mVersion}</div>
    </div>
    <div class="text-black p-4 text-xl col-span-1 row-span-2">
      {Model.mSummary}
    </div>
  </div>
</div>
{:else}
<div class="bg-theme-dark-background rounded-lg">
  <button
        class="text-theme-dark-lightText border-none p-1 rounded cursor-pointer text-xs bg-theme-dark-background hover:bg-theme-dark-background transition-all duration-300 ease-in-out"
        on:click={goBack}> 
          <Icon path={mdiArrowLeftBold} />
        <span class="ml-2"> Back </span>
        </button>
  <div class="grid grid-cols-2 grid-rows-3 bg-theme-dark grid-rows-2 gap-2 p-4 shadow-lg w-full h-full">
    <!-- Video Section -->
    <div class="relative bg-theme-dark-primary rounded-lg block items-center justify-center col-span-1 row-span-2">
      <video src="https://www.pexels.com/download/video/3121459/" class="p-1 rounded-lg" loop autoplay muted playsinline></video>
      <!-- svelte-ignore a11y-img-redundant-alt -->
    </div>
    
    <div class="flex flex-col p-4 col-span-1 row-span-1">
      <div class="text-2xl  text-dark-primary font-bold justify-center ">{Model.mName}</div>
      <div class=" text-theme-dark-white text-base">{Model.mDescription}</div>
      <div class="align-right font-bold text-theme-dark-white justify-right mt-2 text-lg "> Version: {Model.mVersion}</div>
    </div>
    <div class="text-white p-4 text-xl col-span-1 row-span-2">
      {Model.mSummary}
    </div>
  </div>
</div>
{/if}



<style>
  Button:hover{
      color: aliceblue;
        opacity: 1;
        font-weight: 600;
        transition: opacity 0.5s;
    }
 </style>