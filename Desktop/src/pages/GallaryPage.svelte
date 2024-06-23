<script>
  import { onMount } from "svelte";

  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let data = null;

  let videoURLs = [];
  let videoNames = [];
  let downloadedStatuses = [];

  // Fetch the video records from the database
  onMount(async () => {
    isLoading.set(true);
    try {
      const response = await window.electronAPI.fetchVideos();
      if (response.success) {
        videoURLs = response.data.map((record) => record.dataValues.localurl);
        videoNames = response.data.map((record) => record.dataValues.mname);
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

  console.log("At gallery page");
</script>

<ProtectedRoutes>
  {#if $isLoading}
  <div class="flex justify-center">
    <Spinner />
  </div>
  {:else}
    <div class="items-center">
      <div>
        <div
          class="text-4xl font-heading text-theme-dark-bgHover text-center rounded"
        >
          Gallery
        </div>
        <div class="grid grid-flow-row-dense grid-cols-3 items-center">
          {#each videoURLs as url,index}
            <GallaryCard VideoSource={url} VideoName={videoNames[index]} isDownloaded={downloadedStatuses[index]}/>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</ProtectedRoutes>
