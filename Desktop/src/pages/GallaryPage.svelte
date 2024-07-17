<script>
  import { onMount } from "svelte";

  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
  import {filteredItems} from "../stores/filteredItems";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  import {writable} from "svelte/store";

  let data = null;

  let videoURLs = [];
  let videoNames = [];
  let downloadedStatuses = [];

  let searchQuery = '';
  let sortCategory = 'All';

  let videoURLToNameMap = {};

  videoURLs.forEach((url, index) => {
    videoURLToNameMap[url] = videoNames[index];
  });

  // Fetch the video records from the database
  //TODO: Must fecth date and model names as well for filter function
  onMount(async () => {
    isLoading.set(true);
    try {
      const response = await window.electronAPI.fetchVideos();
      if (response.success) {
        videoURLs = response.data.map((record) => record.dataValues.localurl);
        videoNames = response.data.map((record) => record.dataValues.mname);
        // console.log(videoURLs);
        // console.log(videoNames);
        // filteredItems = videoURLs;

        videoURLToNameMap = videoURLs.reduce((acc, url, index) => {
          acc[url] = videoNames[index];
          return acc;
        },{});
        downloadedStatuses = await Promise.all(
          videoURLs.map(async (url) => {
            const checkResponse = await window.electronAPI.checkFileExistence(url);
            if (checkResponse.success) {
              return checkResponse.exists;
            } else {
              console.error("Error checking file existence:", checkResponse.error);
              return false;
            }
          })
        );
        filteredItems.set(videoURLs);        // console.log("Downloaded statuses:", downloadedStatuses);
      } else {
        console.error("Failed to fetch video records:", response.error);
      }
      
      await new Promise((resolve) => setTimeout(resolve, 3000));
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

  
  // $: filteredItems = videoURLs.filter(item => {
  //  const searchRegex = new RegExp(searchQuery, 'i');

  //   if (filterCategory === 'Name') {
  //    return searchRegex.test(videoNames[item]); //TODO: check this (maybe meant to be mname)
  //  } else if (filterCategory === 'Date') {
  //    return searchRegex.test(item.date); //check the returned value
  //  } else if (filterCategory === 'Model Name') {
  //    return searchRegex.test(item.modelName); //check the returned value
  //  }
  //  return true;
  // }); 

   async function handleSearch(event) {
    searchQuery = event.target.value;
    console.log("Search query: " + searchQuery); 
    console.log("Video URLS: " + videoURLs);
    filteredItems.update(() => {
      if (searchQuery === '') {
        // If search query is empty, display all videos
        console.log("Search query is empty, displaying all items.");
        return videoURLs;
      } else {
        const searchRegex = new RegExp(searchQuery, 'i');
        const newItems = videoURLs.filter(url => searchRegex.test(videoURLToNameMap[url]));
        console.log("FilteredItems: " + newItems);
        return newItems;
      }
    });
}

  function sortFilteredItems() {
    filteredItems.update(items => {
      let sortedItems;
      if (sortCategory === 'Name') {
        sortedItems = [...items].sort((a, b) => videoURLToNameMap[a].name.compare(videoURLToNameMap[b].name));
      } else if (sortCategory === 'Date') {
        sortedItems = [...items].sort((a, b) => videoURLToNameMap[b].date - videoURLToNameMap[a].date);
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

</script>

<ProtectedRoutes>
  {#if $isLoading}
  <div class="flex justify-center w-full">
    <Spinner />
  </div>
  {:else}
    <div class="items-center">
      <div>
      <div class="flex justify-center items-center w-full mb-4 p-4 "> <!--TODO: style the searchbar -->
        <input
          type="text"
          placeholder="Search..."
          on:input={handleSearch}
          class="bg-theme-dark-white text-black rounded-lg border-2 border-theme-dark-secondary p-2 w-5/6 border-solid text-lg" 
          />
        <!-- TODO: style filter bar-->
       <!-- <select class="bg-theme-dark-secondary  rounded-lg ml-2 p-2  text-lg" 
          on:change={handleSortChange}
          placeholder="Sort...">
             <option value="All">Sort...</option>
             <option value="Name">Name</option>
             <option value="Date">Date</option>
            <option value="Model Name">Model Name</option>
         </select> -->
      </div>
      {#if $filteredItems.length > 0}
        <div class="grid grid-flow-row-dense lg:grid-cols-3 md:grid-cols-2 grid-cols-1 items-center w-full ">
          {#each $filteredItems as url, index}
            <GallaryCard VideoSource={url} VideoName={videoURLToNameMap[url]} isDownloaded={downloadedStatuses[index]} />
          {/each}
          </div>
        {:else}
          <div class="shadow-card-blue justify-center place-items-center self-center relative overflow-hidden rounded-lg p-2 w-10/12 shadow-theme-keith-accenttwo m-2 ml-auto mr-auto transition-all duration-300 ease-in-out">
            <h3 class="text-center justify-center"> No results for your search. Please try a different term. </h3></div>
        {/if}
        
      </div>
    </div>
  {/if}
</ProtectedRoutes>
