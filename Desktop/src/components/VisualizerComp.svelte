<script>
    import { onMount } from 'svelte';
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";;
    

    let scale = 1;
  let translateX = 0;
  let translateY = 0;
  let isDragging = false;
  let startX = 0;
  let startY = 0;

  const handleWheel = (event) => {
    event.preventDefault();
    scale += event.deltaY * -0.001;
    scale = Math.min(Math.max(1, scale), 5);
  };

  const handleMouseDown = (event) => {
    isDragging = true;
    startX = event.clientX - translateX;
    startY = event.clientY - translateY;
  };

  const handleMouseMove = (event) => {
    if (!isDragging) return;
    translateX = event.clientX - startX;
    translateY = event.clientY - startY;
  };

  const handleMouseUp = () => {
    isDragging = false;
  };
</script>


    
<div class="relative h-screen flex justify-center items-center bg-gray-100">
  <div class="image-container w-full h-full">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img
      src="./images/data.pkl.svg"
      alt="Zoomable Image"
      class="image"
      style="transform: translate({translateX}px, {translateY}px) scale({scale})"
      on:wheel={handleWheel}
      on:mousedown={handleMouseDown}
      on:mousemove={handleMouseMove}
      on:mouseup={handleMouseUp}
      on:mouseleave={handleMouseUp}
    />
  </div>
</div>
  


  <style>
    .image-container {
    overflow: hidden;
    position: relative;
  }
  .image {
    transition: transform 0.1s;
  }
  </style>
  
  
  