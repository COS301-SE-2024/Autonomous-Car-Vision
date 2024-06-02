<script>
  import { Button, Tooltip } from "svelte-materialify";
  // Exported Parameters

  export let Model = {
    name: "",
    category: "",
    description: "",
    status: "",
    gif: "",
    img: "",
  };
  export let key;

  let statusColour = "";
  let status = "";

  if (Model.status === "green") {
    statusColour = "#00DC82";
    status = "Online";
  } else if (Model.status === "orange") {
    statusColour = "#EC9F05";
    status = "Retraining";
  } else if (Model.status === "red") {
    statusColour = "#FF0000";
    status = "Offline";
  }

  let show = false;

  let isHovered = false;

  function handleMouseOver() {
    isHovered = true;
  }

  function handleMouseOut() {
    isHovered = false;
  }
</script>

<div
  {key}
  class="flex flex-col items-start border-2 border-black rounded-xl lg:w-full w-10/12 mx-auto"
>
  <div
    id="header"
    class="flex flex-row items-center justify-between px-6 py-4 w-full"
  >
    <div class="inline-flex flex-row items-center gap-2">
      {#if Model.img !== ""}
        <img
          class="rounded-full"
          src={Model.img}
          alt={Model.name}
          style="height: 53px; width: 52px; object-fit: cover;"
        />
      {:else}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="52"
          height="53"
          viewBox="0 0 32 33"
          fill="none"
        >
          <circle cx="16" cy="16.5" r="16" fill="#DEDEDE" />
        </svg>
      {/if}
      <div class="flex flex-col">
        <p class="w-fit text-black text-xl font-medium">{Model.name}</p>
        <p class="w-40 text-gray text-md font-normal">
          {Model.category}
        </p>
      </div>
    </div>
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
  {#if Model.gif === ""}
    <div
      id="image"
      class="flex justify-center items-center bg-black h-72 w-full"
    >
      <p class="text-center text-gray-light">No model image to display</p>
    </div>
  {:else}
    <div
      id="image"
      class="flex justify-center items-center bg-black h-full w-full"
    >
      <img class="" src={Model.gif} alt={Model.name} />
      <!-- <img height="100%" width="100%"
        src={isHovered ? Model.gif : Model.gif}
        alt="Hover to play GIF"
        on:mouseover={handleMouseOver}
        on:mouseleave={handleMouseOut}
      /> -->
    </div>
  {/if}
  <div id="content" class="flex flex-col gap-4 w-full p-4">
    <div id="withcontent" class="flex flex-col items-start gap-0">
      <h1 class="text-lg font-medium">{Model.name}</h1>
      <p class="font-light h-fit">
        {Model.description}
      </p>
    </div>
    <div id="buttons" class="ml-auto w-8/12 grid grid-cols-2 gap-2">
      <Button class="bg-primary-green-light" rounded depressed>button 2</Button>
      <Button class="bg-primary-green-light" rounded depressed>button 1</Button>
    </div>
  </div>
</div>

<style>
</style>
