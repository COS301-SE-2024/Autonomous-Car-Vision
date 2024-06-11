<script>
  import GallaryCard from "../components/GallaryCard.svelte";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";

  let videoURLs = [];

  // Fetch the video records from the database
  window.electronAPI.fetchVideos().then((response) => {
    if (response.success) {
      videoURLs = response.data.map((record) => record.dataValues.localurl);
    } else {
      console.error("Failed to fetch video records:", response.error);
    }
  });
  console.log("At gallery page");
</script>

<ProtectedRoutes>
  <div class="items-center">
    <div>
      <div
        class="text-xl font-heading text-theme-keith-accentone text-center rounded"
      >
        Video Gallery
      </div>
      <div class="grid grid-flow-row-dense grid-cols-3 items-center">
        {#each videoURLs as url}
          <GallaryCard VideoSource={url} />
        {/each}
      </div>
    </div>
  </div>
</ProtectedRoutes>
