<script>
  import { onMount } from "svelte";

  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";

  import { isGalLoading } from "../stores/galleryLoading";
  import PingLoader from "../components/PingLoader.svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let data = null;

  let videoURLs = [];
  let videoNames = []; 

  // Fetch the video records from the database
  onMount(async () => {
    isGalLoading.set(true);
    isLoading.set(true);
    try {
      // Simulate data fetching with a delay
      window.electronAPI.fetchVideos().then((response) => {
        if (response.success) {
          videoURLs = response.data.map((record) => record.dataValues.localurl);
          videoNames = response.data.map((record) => record.dataValues.mname);
          console.log(videoNames);
        } else {
          console.error("Failed to fetch video records:", response.error);
        }
        setTimeout(() => {
          isGalLoading.set(false);
        }, 1000);
      });
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
            {#if $isGalLoading}
            <div class="flex justify-center">
              <PingLoader />
            </div>
            {/if}
            {#if !$isGalLoading}
              <GallaryCard VideoSource={url} VideoName={videoNames[index]}/>
            {/if}
          {/each}
        </div>
      </div>
    </div>
  {/if}
</ProtectedRoutes>
