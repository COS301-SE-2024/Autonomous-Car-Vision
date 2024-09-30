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

  function detectPlatformDirectory() {
    const platform = os.platform();

    if (platform === "win32") {
      // For Windows, use the AppData directory
      return path.join(process.env.APPDATA, "HVstore");
    } else if (platform === "linux") {
      // For Linux, use ~/.local/share
      return path.join(os.homedir(), ".local", "share", "HVstore");
    } else if (platform === "darwin") {
      // For macOS, use ~/Library/Application Support
      return path.join(
        os.homedir(),
        "Library",
        "Application Support",
        "HVstore",
      );
    } else {
      // Default case for other platforms
      console.warn("Unknown platform. Defaulting to the home directory.");
      return path.join(os.homedir(), "HVstore");
    }
  }

  onMount(async () => {
    isLoading.set(true);
    try {
      const savedPath = await window.electronAPI.getDrivesDirectory();
      if (savedPath) {
        directoryPath = savedPath;

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
      console.error("Failed to get base directory:", error);
    } finally {
      isLoading.set(false);
    }
  });

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
  {:else}
    <div class={$theme === "highVizLight" ? "text-black" : "text-white"}>
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
          {#if directoryPath}
            <p class={$theme === "highVizLight" ? "text-black" : "text-white"}>
              Selected Directory: {directoryPath}
            </p>
          {/if}
        </div>
        {#if listType === "grid"}
          {#if $filteredItems.length > 0}
            <div class="grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1">
              {#each $filteredItems as url}
                <DriveCard
                  {listType}
                  videoSource={url}
                  videoName={videoURLToNameMap[url]}
                />
              {/each}
            </div>
          {:else if directoryPath}
            <div class="shadow-card-blue justify-center">
              <h3 class="text-center">No results for your search.</h3>
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
      </div>
    </div>
  {/if}
</ProtectedRoutes>
