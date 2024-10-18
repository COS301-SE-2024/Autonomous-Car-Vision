<script>
  import { onMount } from "svelte";

  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
  import { filteredItems } from "../stores/filteredItems";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  import { Icon, Button } from "svelte-materialify";
  import { mdiViewList, mdiViewGrid, mdiUpload } from "@mdi/js";
  import UploadModal from "../components/UploadModal.svelte";
  import { theme } from "../stores/themeStore";

  let data = null;

  let videoURLs = [];
  let videoNames = [];
  let downloadedStatuses = [];
  let showModal = false;

  let listType = "grid";

  let searchQuery = "";
  let sortCategory = "All";

  let videoURLToNameMap = {};

  videoURLs.forEach((url, index) => {
    videoURLToNameMap[url] = videoNames[index];
  });

  // Fetch the video records from the database
  onMount(async () => {
    isLoading.set(true);
    const uid = await window.electronAPI.getUid();

    const lastSignin = await window.electronAPI.getLastSignin(uid);
    //TODO: update last signin in the database
    const updateLastSignin = await window.electronAPI.updateLastSignin(uid);

    try {
      const syncSqlite = await window.electronAPI.syncSqlite(uid);
      console.log("syncSqlite", syncSqlite);
    } catch (error) {
      console.error("Failed to sync data", error);
    }
    fetchVideos(uid);
  });

  async function fetchVideos(uid) {
    isLoading.set(true);
    try {
      const response = await window.electronAPI.fetchVideos(uid);
      if (response.success) {
        videoURLs = response.data.map((record) => record.dataValues.localurl);
        videoNames = response.data.map((record) => record.dataValues.mname);
        videoURLToNameMap = videoURLs.reduce((acc, url, index) => {
          acc[url] = videoNames[index];
          return acc;
        }, {});
        downloadedStatuses = await Promise.all(
          videoURLs.map(async (url) => {
            const checkResponse =
              await window.electronAPI.checkFileExistence(url);
            return checkResponse.success ? checkResponse.exists : false;
          }),
        );
        filteredItems.set(videoURLs);
      } else {
        console.error("Failed to fetch video records:", response.error);
      }
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      isLoading.set(false);
    }
  }

  async function handleSearch(event) {
    searchQuery = event.target.value;
    filteredItems.update(() => {
      if (searchQuery === "") {
        // If search query is empty, display all videos
        return videoURLs;
      } else {
        const searchRegex = new RegExp(searchQuery, "i");
        const newItems = videoURLs.filter((url) =>
          searchRegex.test(videoURLToNameMap[url]),
        );
        return newItems;
      }
    });
  }

  function sortFilteredItems() {
    filteredItems.update((items) => {
      let sortedItems;
      if (sortCategory === "Name") {
        sortedItems = [...items].sort((a, b) =>
          videoURLToNameMap[a].name.compare(videoURLToNameMap[b].name),
        );
      } else if (sortCategory === "Date") {
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

  function handleUploadSuccess(event) {
    console.log("Upload successful, re-fetching videos...");
    fetchVideos(); // Re-fetch the video list after upload
  }
</script>

<ProtectedRoutes>
  {#if $isLoading}
    <div class="flex justify-center w-full">
      <Spinner />
    </div>
  {:else if $theme === "highVizLight"}
    <div class="items-center">
      <div>
        <div class="flex justify-between gap-2 items-center w-full mb-4 p-4">
          <!--TODO: style the searchbar -->
          <div class="Card-Or-List rounded-md flex">
            <button
              on:click={() => handleListTypeChange("grid")}
              class={listType === "grid"
                ? "text-highVizDark-secondary"
                : "text-highVizDark-primary"}
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
            class="bg-theme-dark-white text-black rounded-lg border-2 border-highVizDark-secondary p-2 w-5/6 border-solid text-lg"
          />
          <Button
            rounded
            class="bg-dark-primary text-black"
            on:click={() => (showModal = true)}
          >
            Upload
            <Icon color="white" path={mdiUpload} size="30" />
          </Button>
        </div>
        {#if listType === "grid"}
          {#if $filteredItems.length > 0 || $isLoading}
            <div
              class="grid grid-flow-row-dense lg:grid-cols-3 md:grid-cols-2 grid-cols-1 items-center w-full"
            >
              {#each $filteredItems as url, index}
                <GallaryCard
                  {listType}
                  videoSource={url}
                  videoName={videoURLToNameMap[url]}
                  isDownloaded={downloadedStatuses[index]}
                  id="gallery-card"
                />
              {/each}
            </div>
          {:else}
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
            {#each $filteredItems as url, index}
              <GallaryCard
                {listType}
                videoSource={url}
                videoName={videoURLToNameMap[url]}
                isDownloaded={downloadedStatuses[index]}
              />
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {:else}
    <div class="items-center">
      <div>
        <div class="flex justify-between gap-2 items-center w-full mb-4 p-4">
          <!--TODO: style the searchbar -->
          <div class="Card-Or-List rounded-md flex">
            <button
              on:click={() => handleListTypeChange("grid")}
              class={listType === "grid"
                ? "text-highVizDark-secondary"
                : "tex-highVizDark-primary"}
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
            class="bg-theme-dark-white text-black rounded-lg border-2 border-highVizDark-secondary p-2 w-5/6 border-solid text-lg"
          />
          <Button
            rounded
            class="bg-dark-primary text-white"
            on:click={() => (showModal = true)}
          >
            Upload
            <Icon color="white" path={mdiUpload} size="30" />
          </Button>
        </div>
        {#if listType === "grid"}
          {#if $filteredItems.length > 0 || $isLoading}
            <div
              class="grid grid-flow-row-dense lg:grid-cols-3 md:grid-cols-2 grid-cols-1 items-center w-full"
            >
              {#each $filteredItems as url, index}
                <GallaryCard
                  {listType}
                  videoSource={url}
                  videoName={videoURLToNameMap[url]}
                  isDownloaded={downloadedStatuses[index]}
                  id="gallery-card"
                />
              {/each}
            </div>
          {:else}
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
            {#each $filteredItems as url, index}
              <GallaryCard
                {listType}
                videoSource={url}
                videoName={videoURLToNameMap[url]}
                isDownloaded={downloadedStatuses[index]}
              />
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {/if}
  {#if showModal}
    <div class="w-full h-full flex justify-center items-center">
      <UploadModal on:uploadSuccess={handleUploadSuccess} bind:showModal />
    </div>
  {/if}
</ProtectedRoutes>
