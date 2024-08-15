<script>
  import ModelsCard from "../components/ModelsCard.svelte";
  import ModelsCardContent from "../components/ModelsCardContent.svelte";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";
  import { onMount } from "svelte";
  import { selectedModel } from "../stores/modelsStore.js";
  import { get } from "svelte/store";



  let Models = [];
  onMount(async () => {

    isLoading.set(true);
    try {
      const result = await window.electronAPI.getAIModels();
      if (result.success) {
        Models = result.data.map((model) => ({
          mName: model.model_name,
          mDescription: model.model_summary,
          mVersion: model.model_version,
          mSummary: model.model_description,
          mStatus: "green", // Assuming a default status; you can adjust this as needed
          mProfileImg: model.model_profileimg,
          mImg: model.model_img,
        }));
      } else {
        console.error("Failed to fetch AI models:", result.error);
      }
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      isLoading.set(false);
    }
  });


 
  let selected = get(selectedModel);

  function selectModel(model) {
    selected = model;
   }

  function closeModelContent() {
    selected = null;
  }

</script>

<ProtectedRoutes>
  {#if $isLoading}
    <div class="flex justify-center">
      <Spinner />
    </div>
  {:else}
      <div class="grid grid-flow-row-dense lg:grid-cols-3 md:grid-cols-2 grid-cols-1 items-center w-full pl-4 pt-5"
            >
            {#each Models as Model, key}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div on:click={() => selectModel(Model)}>
              <ModelsCard {Model} {key} />
              </div>
            {/each}

        </div>
        {#if selected}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
          <div class="model-content-overlay rounded-lg" on:click{closeModelContent()}>
              <ModelsCardContent {selected} />
          </div>
        {/if}

  {/if}
</ProtectedRoutes>

<style>
  /* @import "../assets/base.css"; */

  .model-content-overlay {
    position: fixed;
    top: 11%;
    left: 18%;
    background-image: linear-gradient(180deg, #001524, #181818);
    z-index: 1000;
    width: 125vh;
    height: 77vh;
  }
</style>