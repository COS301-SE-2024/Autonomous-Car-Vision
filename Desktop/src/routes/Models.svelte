<script>
    import ModelsCard from "../components/ModelsCard.svelte";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";

    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { onMount } from "svelte";

    let Models = [
        {
            name: "AI Model#1",
            category: "Pedestrian Detection",
            version: "Version 1.1",
            moreDetails: "Haike! ke tsona diDetails tsa the AI Model tsona tse. Ke ngola heela ha ke tsebe hore ke batla ho ngwala eng. Empa bo telle ba mongolo ona o tlameile o be motelele.",
            status: "green",
            gif: "",
            img: "",
        },
        {
            name: "AI Model#2",
            category: "Pothole Detection",
            version: " Version 2",
            moreDetails: "HHHHHHEOEJFIHDHBCAJKNSCIABC ",
            status: "orange",
            gif: "",
            img: "",
        },
        {
            name: "AI Model#3",
            category: "Lane Change Model",
            version: "Version 3.4",
            moreDetails: "HHHHHHEOEJFIHDHBCAJKNSCABC ",
            status: "red",
            gif: "https://media1.tenor.com/m/GqOoWCxt5DEAAAAC/fast-car.gif",
            img: "https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        },
    ];

    // let Model = {
    //     name: "AI Model#1",
    //     category: "Object Detection",
    //     version: "Testing the Version of AI Model#1",
    //     status: "green",
    //     svg: "",
    //     img: "",
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
