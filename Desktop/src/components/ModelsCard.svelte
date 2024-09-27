<script>
  import { Button, Tooltip } from "svelte-materialify";
  import ModelsCardContent from "../components/ModelsCardContent.svelte";
  import baffle from "baffle";
   import { onMount } from "svelte";
   import { selectedModel } from "../stores/modelsStore.js"; 
   import {theme} from '../stores/themeStore';


  export let Model = {
    mName: "",
    mDescription: "",
    mVersion: "",
    mSummary: "",
    mStatus: "",
    mProfileImg:
      "https://cdn.pixabay.com/photo/2024/03/11/19/15/ai-generated-8627457_640.png",
    mImg: "",
  };
  export let key;
 
  const script = "https://cdn.jsdelivr.net/npm/baffle@0.3.6/dist/baffle.min.js";

  let b;
  let b1;
  let versionElement;
  let nameElement;
  let animationRunning = false;

  onMount(async ()  => {
    b = baffle('.version', {
      characters: '0909dudcrfds',
      speed: 100
    });
    b.start();
    b.reveal(5000);

    b1 = baffle('.mName', {
      characters: '0909dudedggsedcrfefds',
      speed: 100
    });
    b1.start();
    b1.reveal(5000);
  });

  const handleHover = () => {

    if (!animationRunning) {
      animationRunning = true;

      // Stop any ongoing baffle animation
      b.stop();
      b1.stop();
    

      b = baffle(versionElement, {
        characters: '0909dudcrfds',
        speed: 100        
      });
      b.start();
      b.reveal(5000, () => {
          animationRunning = false;  // Mark as finished after reveal
        });;

      b1 = baffle(nameElement, {
        characters: '0909dudedggsedcrfefds',
        speed: 100
      });
      b1.start();
      b1.reveal(5000, () => {
          animationRunning = false;  // Mark as finished after reveal
        });
      }
  };


  let statusColour = "";
  let status = "";

  if (Model.mStatus === "green") {
    statusColour = "#00DC82";
    status = "Online";
  } else if (Model.mStatus === "orange") {
    statusColour = "#EC9F05";
    status = "Retraining";
  } else if (Model.mStatus === "red") {
    statusColour = "#FF0000";
    status = "Offline";
  }

    
  let show = false;

  let isHovered = false;

  const handleClick = () => {
    selectedModel.set(Model); 
    console.log("handleClick for " + selectedModel.mName);
  };



</script>

{#if $theme === 'highVizLight'}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="cursor-pointer relative grid rounded-lg grid-cols-8 gap-0 flex p-4 shadow-lg background-card w-72 h-96" 
on:click={handleClick}
on:mouseenter={handleHover}>
 <div class="texto col-span-1 transform rotate-180 text-dark-primary">
   {Model.mDescription}
 </div>
 <div class="flex col-span-7 flex-col justify-center w-full h-full">
   <!-- svelte-ignore a11y-img-redundant-alt -->
   <img
     src={Model.mProfileImg}
     alt="Profile Image"
     class="w-full h-3/4 object-cover"
   />
   <div class="block"> 
       <div class="data flex flex-col">
         <div bind:this={versionElement} class="version mt-2 text-sm text-black">-Ver. {Model.mVersion}</div>
          <div bind:this={nameElement}  class="mName text-lg font-bold text-black">{Model.mName}</div>
       </div>
       <div class="absolute bottom-10 left-60 ">
         <Tooltip left bind:active={show}>
           <svg
             xmlns="http://www.w3.org/2000/svg"
             width="16"
             height="17"
             viewBox="0 0 16 17"
             fill="none"
           >
             <circle cx="8" cy="8.5" r="8" fill={statusColour} />
           </svg>
           <span slot="tip">{status}</span>
         </Tooltip>
       </div>
   </div>
 </div>
</div>
{:else}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="cursor-pointer relative grid rounded-lg grid-cols-8 gap-0 flex p-4 shadow-lg background-card w-72 h-96" 
on:click={handleClick}
on:mouseenter={handleHover}>
 <div class="texto col-span-1 transform rotate-180 text-dark-primary">
   {Model.mDescription}
 </div>
 <div class="flex col-span-7 flex-col justify-center w-full h-full">
   <!-- svelte-ignore a11y-img-redundant-alt -->
   <img
     src={Model.mProfileImg}
     alt="Profile Image"
     class="w-full h-3/4 object-cover"
   />
   <div class="block"> 
       <div class="data flex flex-col">
         <div bind:this={versionElement} class="version mt-2 text-sm text-white">-Ver. {Model.mVersion}</div>
          <div bind:this={nameElement}  class="mName text-lg font-bold text-white">{Model.mName}</div>
       </div>
       <div class="absolute bottom-10 left-60 ">
         <Tooltip left bind:active={show}>
           <svg
             xmlns="http://www.w3.org/2000/svg"
             width="16"
             height="17"
             viewBox="0 0 16 17"
             fill="none"
           >
             <circle cx="8" cy="8.5" r="8" fill={statusColour} />
           </svg>
           <span slot="tip">{status}</span>
         </Tooltip>
       </div>
   </div>
 </div>
</div>
{/if}


 


<style>
  /* @import "../assets/base.css"; */

  .background-card {
    /* border: 0.5px solid #012431; */
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  }

  .background-card:hover {
    background-color: #012431b1;
  }

  .texto {
    writing-mode: vertical-rl;
    position: relative;
    -webkit-writing-mode: vertical-rl;
    /* padding-left: 15px; */
  }
</style>
