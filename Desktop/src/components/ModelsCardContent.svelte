<script>
    import { Button, Tooltip } from "svelte-materialify";
    // import { selectedModel } from "../stores/modelsStore";
    // Exported Parameters
   

    
  
    export let Model = {
      mName: "",
      mDescription: "",
      mVersion: "",
      mSummary: "",
      mStatus: "",
      mProfileImg: "https://cdn.pixabay.com/photo/2024/03/11/19/15/ai-generated-8627457_640.png",
      mImg: "",
    };
    //  export let key;

    const goBack = () => {
      selectedModel.set(null);
    };
</script>

<div>
  <Button
        class=" text-theme-dark-lightText border-none p-2 rounded cursor-pointer text-xs bg-theme-dark-primary hover:bg-theme-dark-secondary transition-all duration-300 ease-in-out"
        on:click={goBack}>Back</Button
      >
  <div class="grid grid-cols-2 bg-theme-dark grid-rows-2 gap-2 p-4 shadow-lg w-full h-full">
    <!-- Video Section -->
    <div class="relative bg-theme-dark-primary rounded-lg block items-center justify-center">
      <video src="https://www.pexels.com/download/video/3121459/" class="p-1 rounded-lg" loop autoplay muted playsinline></video>
      <!-- svelte-ignore a11y-img-redundant-alt -->
    </div>
    
    <!-- Model Name and Description -->
    <div class="flex flex-col p-4 ">
      <div class="text-xl  text-theme-dark-lightText font-bold justify-center ">{Model.mName}</div>
      <div class=" text-theme-dark-lightText">{Model.mDescription}</div>
      <div class="align-right text-theme-dark justify-right mt-2 text-lg "> {Model.mVersion}</div>
    </div>
    
    <!-- Summary -->
    <div class="text-theme-dark p-4">
      {Model.mSummary}
    </div>
    
    <!-- Placeholder for Dashboard -->
    <div class="text-theme-dark bg-theme-dark-primary rounded-lg flex items-center justify-center">
      <span>placeholder for dashboard {Model.mName}</span>
    </div>
  </div>
</div>


<style>
     @import '../assets/base.css';
 </style>