<script>
  import { onMount } from "svelte";

  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  import {writable} from "svelte/store";

  let data = null;

  let videoURLs = [];
  let videoNames = [];
  let downloadedStatuses = [];

  let searchQuery = '';
  let filterCategory = 'All';

  // Fetch the video records from the database
  //TODO: Must fecth date and model names as well for filter function
  onMount(async () => {
    isLoading.set(true);
    try {
      const response = await window.electronAPI.fetchVideos();
      if (response.success) {
        videoURLs = response.data.map((record) => record.dataValues.localurl);
        videoNames = response.data.map((record) => record.dataValues.mname);
        console.log(videoURLs);
        console.log(videoNames);
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
        console.log("Downloaded statuses:", downloadedStatuses);
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

  
  $: filteredItems = videoURLs.filter(item => {
   const searchRegex = new RegExp(searchQuery, 'i');

    if (filterCategory === 'Name') {
     return searchRegex.test(videoNames[item]); //TODO: check this (maybe meant to be mname)
   } else if (filterCategory === 'Date') {
     return searchRegex.test(item.date); //check the returned value
   } else if (filterCategory === 'Model Name') {
     return searchRegex.test(item.modelName); //check the returned value
   }
   return true;
  }); 

  function handleSearch(event) {
    searchQuery = event.target.value;
    filteredItems = videoURLs.filter(item => {
      const searchRegex = new RegExp(searchQuery, 'i');

      if (filterCategory === 'Name') {
        return searchRegex.test(videoNames[item]);
      } else if (filterCategory === 'Date') {
        return searchRegex.test(item.date);
      } else if (filterCategory === 'Model Name') {
        return searchRegex.test(item.modelName);
      }
      return true;
    });
  }

  function handleFilterChange(event) {
    filterCategory = event.target.value;
  }

</script>

<ProtectedRoutes>
  {#if $isLoading}
  <div class="flex justify-center">
    <Spinner />
  </div>
  {:else}
    <div class="items-center">
      <div>
      <div class="flex justify-center items-center w-full mb-4 p-4 "> <!--TODO: style the searchbar -->
        <input
          type="text"
          placeholder="Search..."
          on:input{handleSearch}
          class="bg-theme-dark-white rounded-lg border-2 border-theme-dark-secondary p-2 w-5/6 border-solid text-lg" 
          />
        <!-- TODO: style filter bar-->
        <select class="bg-theme-dark-secondary  rounded-lg ml-2 p-2  text-lg" 
          on:change={handleFilterChange}
          placeholder="Filter...">
            <option value="All">Filter...</option>
            <option value="Name">Name</option>
            <option value="Date">Date</option>
            <option value="Model Name">Model Name</option>
        </select>
      </div>
        <div class="grid grid-flow-row-dense grid-cols-3 items-center">
        
        {#each filteredItems as url,index} 
            <GallaryCard VideoSource={url} VideoName={videoNames[index]} isDownloaded={downloadedStatuses[index]}/>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</ProtectedRoutes>
