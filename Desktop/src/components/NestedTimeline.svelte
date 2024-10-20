<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let models = [
    {
      id: 1,
      name: "Mod.1",
      profileImg:
        "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      TimeStamp: "Jul 8, 2015",
      Version: 1.4,
    },
    {
      id: 2,
      name: "Mod.2",
      profileImg:
        "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      TimeStamp: "Aug 8, 2015",
      Version: 1.4,
    },
    {
      id: 3,
      name: "Mod.3",
      profileImg:
        "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      TimeStamp: "May 8, 2015",
      Version: 1.8,
    },
    {
      id: 4,
      name: "Mod.4",
      profileImg:
        "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      TimeStamp: "Jun 10, 2024",
      Version: 2.6,
    },
    {
      id: 5,
      name: "Mod.5",
      profileImg:
        "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      TimeStamp: "Jun 8, 2015",
      Version: 1.4,
    },
  ];

  function selectModel(model) {
    dispatch("select", model);
  }
</script>

<div
  class="bg-theme-keith-primary border border-gray-300 shadow-lg p-4 z-50 flex flex-col rounded-lg"
>
  {#each models as model}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="grid grid-cols-4 mb-2 cursor-pointer flex items-center border-b border-theme-keith-accenttwo"
      on:click={() => selectModel(model)}
    >
      <img
        src={model.profileImg}
        alt="Model Profile"
        class="rounded-full model-img"
      />
      <div class="flex flex-col col-span-2 pl-2">
        <p class="text-xs">{model.name}</p>
        <p class="text-xs">{model.TimeStamp}</p>
      </div>
      <div class="relative h-8">
        <p class="text-xs w-min absolute bottom-0 right-0">{model.Version}</p>
      </div>
    </div>
  {/each}
</div>

<style>
  .model-img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 50%;
  }
</style>
