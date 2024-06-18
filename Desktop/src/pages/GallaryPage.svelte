<script>
  import { onMount } from "svelte";

  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";

  import { isGalLoading } from "../stores/galleryLoading";
  import PingLoader from "../components/PingLoader.svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let data = null;

  isGalLoading.set(true);
  let videoURLs = [];

  // Fetch the video records from the database
  onMount(async () => {
    isLoading.set(true);
    try {
      // Simulate data fetching with a delay
      window.electronAPI.fetchVideos().then((response) => {
        if (response.success) {
          videoURLs = response.data.map((record) => record.dataValues.localurl);
        } else {
          console.error("Failed to fetch video records:", response.error);
        }
        setTimeout(() => {
          isGalLoading.set(false);
        }, 4000);
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
          class="text-xl font-heading text-theme-keith-accentone text-center rounded"
        >
          Video Gallery
        </div>
        <div class="grid grid-flow-row-dense grid-cols-3 items-center">
          {#each videoURLs as url}
            {#if $isGalLoading}
            <div class="flex justify-center">
              <PingLoader />
            </div>
            {/if}
            {#if !$isGalLoading}
              <GallaryCard VideoSource={url} />
            {/if}
          {/each}
        </div>
      </div>
    </div>
  {/if}
</ProtectedRoutes>
