<script>
  import { onMount } from "svelte";
  import DriveCard from "../components/DriveCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
  import { filteredItems } from "../stores/filteredItems";
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";
  import { Icon } from "svelte-materialify";
  import { mdiViewList, mdiViewGrid } from "@mdi/js";
  import { theme } from "../stores/themeStore";

  let data = null;
  let directoryPath = "";

  let videoURLs = [];
  let videoNames = [];

  let listType = "grid";
  let searchQuery = "";
  let sortCategory = "All";

  let videoURLToNameMap = {};

  async function openDirectory() {
    directoryPath = await window.electronAPI.selectDrivesDirectory();
    // Update state or do something with the new directory path
  }

  onMount(async () => {
    isLoading.set(true);
    try {
      const savedPath = await window.electronAPI.getDrivesDirectory();
      if (savedPath) {
        directoryPath = savedPath;
        console.log("Saved Directory Path:", directoryPath);

        // Fetch video files from the directory
        const videos = await window.electronAPI.getDriveVideos(directoryPath);

        // Populate videoURLs and videoNames
        videoURLs = videos.map((video) => video.path);
        videoNames = videos.map((video) => video.name);

        // Create a map for easy lookup of names by URL
        videoURLToNameMap = videoURLs.reduce((acc, url, index) => {
          acc[url] = videoNames[index];
          return acc;
        }, {});

        // Update filteredItems store
        filteredItems.set(videoURLs);
      } else {
        // Prompt user to select a directory if none is saved
        await openDirectory();
      }

      data = await fetchData();
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      isLoading.set(false);
    }
  });

  async function fetchData() {
    // Replace with your actual data fetching logic
    return { message: "Data loaded successfully" };
  }

  function handleSearch(event) {
    searchQuery = event.target.value;
    filteredItems.update(() => {
      if (searchQuery === "") {
        return videoURLs;
      } else {
        const searchRegex = new RegExp(searchQuery, "i");
        return videoURLs.filter((url) =>
          searchRegex.test(videoURLToNameMap[url]),
        );
      }
    });
  }

  function sortFilteredItems() {
    filteredItems.update((items) => {
      let sortedItems;
      if (sortCategory === "Name") {
        sortedItems = [...items].sort((a, b) =>
          videoURLToNameMap[a].localeCompare(videoURLToNameMap[b]),
        );
      } else if (sortCategory === "Date") {
        // Assume date info is available and parse appropriately
        sortedItems = [...items].sort(
          (a, b) => videoURLToNameMap[b].date - videoURLToNameMap[a].date,
        );
      } else {
        sortedItems = items;
      }
      return sortedItems;
    });
  }

  function handleSortChange(event) {
    sortCategory = event.target.value;
    console.log("Sort criteria: " + sortCategory);
    sortFilteredItems();
  }

  function handleListTypeChange(type) {
    listType = type;
  }
</script>

<ProtectedRoutes>
  {#if $isLoading}
    <div class="flex justify-center w-full">
      <Spinner />
    </div>
  {:else if $theme === "highVizLight"}
    <div class="items-center text-black">
      <div>
        <div class="flex justify-start gap-2 items-center w-full mb-4 p-4">
          <div class="Card-Or-List rounded-md flex">
            <button
              on:click={() => handleListTypeChange("grid")}
              class={listType === "grid"
                ? "text-dark-secondary"
                : "text-dark-primary"}
            >
              <Icon path={mdiViewGrid} size="30" />
            </button>
            <button
              on:click={() => handleListTypeChange("list")}
              class={listType === "list"
                ? "text-dark-secondary"
                : "text-dark-primary"}
            >
              <Icon path={mdiViewList} size="30" />
            </button>
          </div>
          <input
            type="text"
            placeholder="Search..."
            on:input={handleSearch}
            class="bg-theme-dark-white text-black rounded-lg border-2 border-theme-dark-secondary p-2 w-5/6 border-solid text-lg"
          />
          <button
            class="bg-dark-secondary p-1 rounded-full text-sm"
            on:click={openDirectory}>Select Directory</button
          >
          {#if directoryPath}
            <p class="text-black">Selected Directory: {directoryPath}</p>
          {/if}
        </div>
        {#if listType === "grid"}
          {#if $filteredItems.length > 0}
            <div
              class="grid grid-flow-row-dense lg:grid-cols-3 md:grid-cols-2 grid-cols-1 items-center w-full"
            >
              {#each $filteredItems as url}
                <DriveCard
                  {listType}
                  videoSource={url}
                  videoName={videoURLToNameMap[url]}
                />
              {/each}
            </div>
          {:else if directoryPath}
            <div
              class="shadow-card-blue justify-center place-items-center self-center relative overflow-hidden rounded-lg p-2 w-10/12 shadow-theme-keith-accenttwo m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
            >
              <h3 class="text-center justify-center">
                No results for your search. Please try a different term.
              </h3>
            </div>
          {/if}
        {:else}
          <div class="grid grid-cols-1 gap-4">
            {#each $filteredItems as url}
              <DriveCard
                {listType}
                videoSource={url}
                videoName={videoURLToNameMap[url]}
              />
            {/each}
          </div>
        {/if}
        {#if !directoryPath}
          <div class="flex flex-col justify-center items-center">
            <h1 class="text-3xl">
              Please select a Drive directory before proceeding
            </h1>
            <button
              class="bg-dark-secondary p-2 rounded-full text-lg w-4/12"
              on:click={openDirectory}>Select Directory</button
            >
          </div>
        {/if}
      </div>
    </div>
  {:else}
    <div class="items-center text-white">
      <div>
        <div class="flex justify-start gap-2 items-center w-full mb-4 p-4">
          <div class="Card-Or-List rounded-md flex">
            <button
              on:click={() => handleListTypeChange("grid")}
              class={listType === "grid"
                ? "text-dark-secondary"
                : "text-dark-primary"}
            >
              <Icon path={mdiViewGrid} size="30" />
            </button>
            <button
              on:click={() => handleListTypeChange("list")}
              class={listType === "list"
                ? "text-dark-secondary"
                : "text-dark-primary"}
            >
              <Icon path={mdiViewList} size="30" />
            </button>
          </div>
          <input
            type="text"
            placeholder="Search..."
            on:input={handleSearch}
            class="bg-theme-dark-white text-black rounded-lg border-2 border-theme-dark-secondary p-2 w-5/6 border-solid text-lg"
          />
          <button
            class="bg-dark-secondary p-1 rounded-full text-sm"
            on:click={openDirectory}>Select Directory</button
          >
          {#if directoryPath}
            <p class="text-white">Selected Directory: {directoryPath}</p>
          {/if}
        </div>
        {#if listType === "grid"}
          {#if $filteredItems.length > 0}
            <div
              class="grid grid-flow-row-dense lg:grid-cols-3 md:grid-cols-2 grid-cols-1 items-center w-full"
            >
              {#each $filteredItems as url}
                <DriveCard
                  {listType}
                  videoSource={url}
                  videoName={videoURLToNameMap[url]}
                />
              {/each}
            </div>
          {:else if directoryPath}
            <div
              class="shadow-card-blue justify-center place-items-center self-center relative overflow-hidden rounded-lg p-2 w-10/12 shadow-theme-keith-accenttwo m-2 ml-auto mr-auto transition-all duration-300 ease-in-out"
            >
              <h3 class="text-center justify-center">
                No results for your search. Please try a different term.
              </h3>
            </div>
          {/if}
        {:else}
          <div class="grid grid-cols-1 gap-4">
            {#each $filteredItems as url}
              <DriveCard
                {listType}
                videoSource={url}
                videoName={videoURLToNameMap[url]}
              />
            {/each}
          </div>
        {/if}
        {#if !directoryPath}
          <div class="flex flex-col justify-center items-center">
            <h1 class="text-3xl">
              Please select a Drive directory before proceeding
            </h1>
            <button
              class="bg-dark-secondary p-2 rounded-full text-lg w-4/12"
              on:click={openDirectory}>Select Directory</button
            >
          </div>
        {/if}
      </div>
    </div>
  {/if}
</ProtectedRoutes>
