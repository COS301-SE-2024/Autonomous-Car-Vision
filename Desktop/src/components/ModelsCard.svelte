<script>
  import { Button, Tooltip } from "svelte-materialify";
  // Exported Parameters

  export let Model = {
    mName: "",
    mDescription: "",
    mVersion: "",
    mSummary: "",
    mStatus: "",
    mProfileImg: "",
    mImg: "",
  };
  export let key;
  let isFlipped = false;

  let statusColour = "";
  let status = "";

  function flipCard(){
    isFlipped =!isFlipped;
  }

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

  function handleMouseOver() {
    isHovered = true;
  }

  function handleMouseOut() {
    isHovered = false;
  }
</script>

  <div
    {key}
    class="flex flex-col items-start  border-2 border-theme-blue-light rounded-xl lg:w-full w-10/12 mx-auto text-theme-blue-light"
    on:mouseover={flipCard} on:mouseout={flipCard}>
  <div class="card-inner {isFlipped ? 'flipped' : '' }  rounded-xl ">

    <div class="card-front   rounded-xl  "> 
    <div
      id="header"
      class="flex flex-row  justify-between px-6 py-4 w-full"
    >
      <div class="inline-flex flex-row gap-2">
        {#if Model.mProfileImg !== ""}
          <mImg
            class="rounded-full"
            src={Model.mProfileImg}
            alt={Model.mName}
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
          <p class="w-fit text-theme-blue-light text-xl font-medium">{Model.mName}</p>
          <p class="w-80 text-gray text-md font-normal">
            {Model.mDescription}
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
        <span slot="tip">{Model.mStatus}</span>
      </Tooltip>
    </div>
    {#if Model.mImg === ""}
      <div
        id="image"
        class="flex justify-center items-center bg-black h-72 w-full"
      >
        <p class="text-center text-gray-light">No model image to display</p>
      </div>
    {:else}
      <div
        id="image"
        class="flex justify-center items-center bg-black h-72 w-full"
      >
        <mImg class="h-72 w-full" src={Model.mImg} alt={Model.mName} />
       </div>
    {/if}
    <div id="content" class="flex flex-col gap-4 w-full p-4">
      <div id="withcontent" class="flex flex-col items-start gap-0">
        <h1 class="text-lg font-medium">{Model.mVersion}</h1>
        <!--p class="font-light h-fit">
          {Model.mVersion}
        mSummary</p-->
      </div>
    </div>
    </div>
    <div class="card-back rounded-xl">
     <div class="flex flex-row items-center justify-between px-6 py-4 w-full">
       <p class="font-light h-fit"> {Model.mSummary} </p>
    </div>
   
       </div>
  </div>
</div>
 

<style>


.card-inner{
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  transform: rotateY(0deg);
}

.card-inner.flipped{
  transform: rotateY(180deg);
}

.card-front, card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}

.card-front {
  background-color: #fff;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}

.card-back {
  background-color: #fff;
  transform: rotateY(180deg);
  backface-visibility: hidden;
  width: 100%;
  height: 100%;
  padding: 10px;
}

</style>
