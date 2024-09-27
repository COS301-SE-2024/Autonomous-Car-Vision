<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { VideoURL } from "../stores/video";
  import { createEventDispatcher } from "svelte";
  import { push } from "svelte-spa-router";
  import {theme} from '../stores/themeStore';

  const dispatch = createEventDispatcher();

  export let imgSource;
  export let videoSource;
  export let videoName;

  onMount(() => {
    VideoURL.set(videoSource);
  })

  function back(event) {
    event.stopPropagation(); // Stop event propagation
    dispatch("close");
  }

  function view(videoSource) {
    console.log("TESTING", videoSource);
    const encodedPath = encodeURIComponent(videoSource);
    push(`/video/${encodedPath}`);
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
  class="fixed inset-0 flex items-center justify-center z-50 bg-modal"
  on:click|stopPropagation={back}
>
  <div
    class="relative bg-white p-8 rounded-lg shadow-lg w-full max-w-2xl border border-theme-keith-primary"
  >
    <div>
      <button
        class="text-white border-none p-2 rounded cursor-pointer text-xs bg-theme-dark-primary hover:bg-theme-dark-secondary transition-all duration-300 ease-in-out"
        on:click={back}>Back</button
      >
    </div>
    <div class="flex flex-col items-center mb-4">
      <img
        src={imgSource}
        alt="video thumbnail"
        class="w-4/5 cursor-pointer"
        on:click={view(videoSource)}
      />
      <p class="mt-4">{videoName}</p>
    </div>
  </div>
</div>
