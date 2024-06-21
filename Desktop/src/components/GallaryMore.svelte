<script>
  import { writable } from "svelte/store";
  import EditVideoModal from "./EditVideoModal.svelte";
  import DeleteModal from "./DeleteModal.svelte";
  import ModelList from "./ModelList.svelte";
  import ViewVideoModal from "./ViewVideoModal.svelte";
  import { createEventDispatcher } from "svelte";
  import { push } from "svelte-spa-router";

  const dispatch = createEventDispatcher();
  const currentTab = writable("original");
  const showModelList = writable(false);
  let selectedModel = null;

  export let imgSource;
  export let videoSource;

  function back(event) {
    event.stopPropagation(); // Stop event propagation
    dispatch("close");
  }

  function switchTab(tab) {
    currentTab.set(tab);
  }

  function view(videoSource) {
    push(`/video/${videoSource}`);
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
  class="fixed inset-0 flex items-center justify-center z-50"
  on:click|stopPropagation={back}
>
  <div
    class="relative bg-theme-keith-secondary p-8 rounded-lg shadow-lg w-full max-w-2xl border border-theme-keith-primary"
  >
    <div>
      <button
        class="text-white border-none p-2 rounded cursor-pointer text-xs bg-theme-keith-accentone hover:bg-theme-keith-accenttwo transition-all duration-300 ease-in-out"
        on:click={back}>Back</button
      >
    </div>
    <div class="flex flex-col items-center mb-4">
        <img src={imgSource} alt="video thumbnail" class="w-4/5 cursor-pointer" on:click={view(videoSource)} />
      <p class="mt-4">Details here</p>
    </div>

  </div>
</div>
