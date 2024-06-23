<script>
    import ModelsCard from "../components/ModelsCard.svelte";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { onMount } from "svelte";

    let Models = [];

    onMount(async () => {
        isLoading.set(true);
        try {
            const result = await window.electronAPI.getAIModels();
            if (result.success) {
                Models = result.data.map(model => ({
                    mName: model.model_name,
                    mDescription: model.model_summary,
                    mVersion: model.model_version,
                    mSummary: model.model_description,
                    mStatus: "green", // Assuming a default status; you can adjust this as needed
                    mProfileImg: model.model_profileimg,
                    mImg: model.model_img,
                }));
            } else {
                console.error('Failed to fetch AI models:', result.error);
            }
        } catch (error) {
            console.error("Failed to fetch data", error);
        } finally {
            isLoading.set(false);
        }
    });
</script>

<ProtectedRoutes>
    {#if $isLoading}
        <div class="flex justify-center">
            <Spinner />
        </div>
    {:else}
        <div class="grid grid-cols-2 gap-6 h-screen py-4 px-4">
            {#each Models as Model, key}
                <ModelsCard {Model} {key} />
            {/each}
        </div>
    {/if}
</ProtectedRoutes>