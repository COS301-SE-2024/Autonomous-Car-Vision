<script>
  import NetworkVisualizer from '../components/VisualizerComp.svelte'
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
  import { writable } from 'svelte/store';

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

// Store for tracking the open topic index
const openTopic = writable(null);

// Function to toggle the topic details view
function toggleTopic(index) {
    openTopic.update((current) => (current === index ? null : index));
}
</script>

<ProtectedRoutes >
  <div class="main">
    <h1> Interactive Network Visualizer</h1>

    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(0)}>
      <span>yolov8s</span>
      <button class="dropdown-btn">
          {#if $openTopic === 0}▲{:else}▼{/if}
      </button>
      <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 0 ? 'open' : '' }">
        <div class="relative h-screen flex justify-center items-center bg-gray-100">
          <div class="image-container w-full h-full">
            <!-- svelte-ignore a11y-img-redundant-alt -->
            <img
              src="./images/yolov8s.svg"
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
      </div>
  </div>

  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(1)}>
    <span>yolov8n</span>
    <button class="dropdown-btn">
        {#if $openTopic === 1}▲{:else}▼{/if}
    </button>
    <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 1 ? 'open' : '' }">
      <div class="relative h-screen flex justify-center items-center bg-gray-100">
        <div class="image-container w-full h-full">
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <img
            src="./images/yolov8s.svg"
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
    </div>
</div>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(2)}>
  <span>yolov8n-seg</span>
  <button class="dropdown-btn">
      {#if $openTopic === 2}▲{:else}▼{/if}
  </button>
  <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 2 ? 'open' : '' }">
    <div class="relative h-screen flex justify-center items-center bg-gray-100">
      <div class="image-container w-full h-full">
        <!-- svelte-ignore a11y-img-redundant-alt -->
        <img
          src="./images/yolov8s.svg"
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
  </div>
</div>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="topic-title w-fit text-theme-blue-light text-xl font-medium" on:click={() => toggleTopic(3)}>
  <span>HV1</span>
  <button class="dropdown-btn">
      {#if $openTopic === 3}▲{:else}▼{/if}
  </button>
  <div class="topic-details text-gray text-md font-normal pl-10 { $openTopic === 3 ? 'open' : '' }">
    <div class="relative h-screen flex justify-center items-center bg-gray-100">
      <div class="image-container w-full h-full">
        <!-- svelte-ignore a11y-img-redundant-alt -->
        <img
          src="./images/yolov8s.svg"
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
  </div>
</div>
    
  </div> 
</ProtectedRoutes>

<style>
  .main {
    text-align: center;
    padding: 1em;
    max-width: 800px;
    margin: 0 auto;
  }

  h1 {
    color: #ffffff;
  }

  .topic {
        border: 1px solid #ccc;
        border-radius: 8px;
        margin-bottom: 10px;
        padding: 10px;
        position: relative;
    }

    .topic-title {
        display: block;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }

    .topic-details {
        margin-top: 10px;
        display: none;
    }

    .topic-details.open {
        display: block;
    }

    .dropdown-btn {
        background: none;
        border: none;
        font-size: 16px;
        cursor: pointer;
    }

    .image-container {
    overflow: hidden;
    position: relative;
  }
  .image {
    transition: transform 0.1s;
  }
</style>