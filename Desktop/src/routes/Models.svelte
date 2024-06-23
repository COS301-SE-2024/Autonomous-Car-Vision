<script>
    import ModelsCard from "../components/ModelsCard.svelte";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";

    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { onMount } from "svelte";

    let Models = [
        {
            mName: "AI Model#1",
            mDescription: "Pedestrian Detection",
            mVersion: "v1.1",
            mSummary: "Haike! ke tsona diDetails tsa the AI Model tsona tse. Ke ngola heela ha ke tsebe hore ke batla ho ngwala eng. Empa bo telle ba mongolo ona o tlameile o be motelele.",
            mStatus: "green",
            mProfileImg: "",
            mImg: "",
        },
        {
            mName: "AI Model#2",
            mDescription: "Pothole Detection",
            mVersion: "v2.0",
            mSummary: "HHHHHHEOEJFIHDHBCAJKNSCIABC ",
            mStatus: "orange",
            mProfileImg: "",
            mImg: "",
        },
        {
            mName: "AI Model#3",
            mDescription: "Lane Change Model",
            mVersion: "v3.4",
            mSummary: "HHHHHHEOEJFIHDHBCAJKNSCABC ",
            mStatus: "red",
            mImg: "https://media1.tenor.com/m/GqOoWCxt5DEAAAAC/fast-car.gif",
            mProfileImg: "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
    ];

    // let Model = {
    //     mName: "AI Model#1",
    //     mDescription: "Object Detection",
    //     mVersion: "Testing the Version of AI Model#1",
    //     mStatus: "green",
    //     mImg: "",
    // };

    onMount(async () => {
        isLoading.set(true);
        try {
            await new Promise((resolve) => setTimeout(resolve, 3000));
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
