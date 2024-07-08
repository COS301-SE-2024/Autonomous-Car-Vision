<script>
  import { Button, Tooltip } from "svelte-materialify";
  // Exported Parameters

  export let Model = {
    mName: "",
    mDescription: "",
    mVersion: "",
    mSummary: "",
    mStatus: "",
    mProfileImg: "https://deep-image.ai/_next/static/media/app-info-generator.bf08e63e.webp",
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

  // onMount(async () => {
  //     try {
  //     await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/imagesloaded.pkgd.min.js');
  //     await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/charming.min.js');
  //     await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/TweenMax.min.js');
  //     await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/demo.js');
  //     console.log('All scripts loaded successfully');
  //     } catch (error) {
  //     console.error(error);
  //     }
  // })

</script>

  <div class="slide flex w-full pointer-events-none cursor-pointer relative h-full bg-white border rounded-lg shadow-md ">
    <div class="slide__img-wrap absolute w-100 h-4/5 self-center relative">
      <mImg src={Model.mProfileImg} class="slide__img w-full h-full left-0 top-0 absolute pointer-events-none"/>
    </div>
    <div class="slide__side">{Model.mDescription}</div>
      <div class="slide__title-wrap w-full relative self-end z-1000">
        <span class="slide__number block text-xl font-bold">Version: {Model.mVersion}</span>
        <h3 class="slide__title text-2xl font-extrabold ">{Model.mName}</h3>
    </div>
  </div>


<div class="content fixed left-0 w-full pointer-events-none z-100">
  <div class="content__item absolute top-0 right-0 w-full h-full overflow-auto">
    <span class="content__number font-bold">Version: {Model.mVersion}</span>
        <h3 class="content__title font-extrabold ">{Model.mName}</h3>
        <div class="content__text">{Model.mSummary}</div>
  </div>
  <button class="content__close absolute bg-none b-0 m-o p-0">
    <svg class="icon icon--longarrow">
      <use xlink:href="#icon-longarrow"></use>
    </svg>
  </button>
</div>

<style>
  .slide {
   grid-area: slide/* Adjust height as needed */
  }

  .slide__img-wrap{
    margin: -40px 0 0 0;
  	right: -20px;
  }

  .slide__img {
    /* background-image: url('{Model.mProfileImg}') !important; */
    background-size: cover;
    background-position: 50% 50%;
    transform: scale3d(1.01,1.01,1);
  }

.js .slide__img-wrap, 
.js .slide__title-wrap,
.js .slide__side {
	opacity: 0;
	pointer-events: none;
}

.js .slide--current .slide__img-wrap {
	opacity: 1;
	pointer-events: auto;
}

.slide--visible .slide__img-wrap {
	pointer-events: auto;
}

.slide__number::before {
	content: "\2014";
	display: inline-block;
	margin: 0 1rem 0 0;
}

.slide__title,
.slide__side {
	display: none;
}

.content {
	top: 10rem;
	height: calc(100% - 10rem);
	pointer-events: none;
}

.content__item{
	padding: 10vh 5vw;
}

.content__item--current,
.content__item--current ~ .content__close {
	pointer-events: auto;
}

.content__title{
  margin: 0.5rem 0;
}

.content__text{
  font-size: 0.85rem;
}

.content__close{
  top: 1rem;
  left: 1rem;
  color: currentColor;
}

.content__close:focus {
	outline: none;
}

.content__number::before {
	content: "\2014";
	display: inline-block;
	margin: 0 1rem 0 0;
}


.content__title {
	margin: 0.5rem 0;
	font-size: 2rem;
}


.js .content__title,
.js .content__number,
.js .content__text,
.js .content__close {
	opacity: 0;
}

@media screen and (min-width: 53em) {
  .slide {
		padding: 10vh 0 7vh;
		flex-direction: column;
		justify-content: space-between;
	}
	.slide__side {
		margin: 0 0 0 -1.85rem;
	}
	.slide__title-wrap {
		margin: 0 0 0 -1.85rem;
	}
	.slide__title,
	.slide__subtitle,
	.slide__side {
		display: block;
	}
	.slide__title {
		font-size: 3.25rem;
		margin: 0 0 0.25rem;
	}
	.slide__side {
		color: var(--color-side);
		position: relative;
		-webkit-writing-mode: vertical-rl;
		writing-mode: vertical-rl;
		transform: rotate(180deg);
		z-index: 1000;
	}
	.content {
		top: 0;
		height: 100%;
	}
	.content__item {
		padding: calc(10vh + 5rem) 0 7vh;
		width: 50.5%;
		right: 7.5%;
		overflow: visible;
	}
	.content__close {
		left: 42%;
		top: calc(10vh + 1rem);
	}
	.content__number {
		position: absolute;
		bottom: 7vh;
		right: 0;
		font-size: 2rem;
	}
	.content__title {
		font-size: 7vw;
	}
	.content__text {
		font-size: 0.95rem;
		column-count: 2;
		column-gap: 2rem;
		max-width: 600px;
		text-align: justify;
	}
}

  /* .header {
     
  } */

  /* .profile-image {
  } */

  /* .status-dot {
    @apply ;
  } */

  /* .status-active {
    background-color: green;
  }

  .status-inactive {
    background-color: red;
  } */

  /* .details {
     ;
  } */

  /* .model-name {
     ;
  } */

  /* .timestamp {
    ;
  } */

  /* .version {
    ;
  } */

  /* .actions {
   ;
  } */

  /* .action-button {
    ;
  } */
</style>

  <!-- svelte-ignore a11y-mouse-events-have-key-events -->
  <!-- <div
    {key}
    class="flex flex-col h-fit items-start  border-2 border-theme-blue-light rounded-xl lg:w-full w-10/12 mx-auto text-theme-blue-light"
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
        <img class="h-72 w-full" src={Model.mImg} alt={Model.mName} />
       </div>
    {/if}
    <div id="content" class="flex flex-col gap-4 w-full p-4">
      <div id="withcontent" class="flex flex-col items-start gap-0">
        <h1 class="text-lg font-medium">{Model.mVersion}</h1>
        <!--p class="font-light h-fit">
          {Model.mVersion}
        mSummary</p>
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

</style> -->
