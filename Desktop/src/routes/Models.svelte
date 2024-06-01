<script>
    import { each } from "svelte/internal";
    import ModelsCard from "../components/ModelsCard.svelte";

    let Models = [
        {
            name: "AI Model#1",
            category: "Pedestrian Detection",
            description: "Testing the Description of AI Model#1",
            status: "green",
            gif: "",
            img: "",
        },
        {
            name: 'AI Model#2',
            category: 'Pothole Detection',
            description: 'Testing the Description of AI Model#2',
            status: 'orange',
            gif: '',
            img: ''
        },
        {
            name: 'AI Model#3',
            category: 'Lane Change Model',
            description: 'Testing the Description of AI Model#3',
            status: 'red',
            gif: 'https://media1.tenor.com/m/GqOoWCxt5DEAAAAC/fast-car.gif',
            img: ''
        }
    ];

    // let Model = {
    //     name: "AI Model#1",
    //     category: "Object Detection",
    //     description: "Testing the Description of AI Model#1",
    //     status: "green",
    //     svg: "",
    //     img: "",
    // };
</script>

<div
    class="grid grid-cols-2 gap-2 h-screen overflow-y-scroll py-4 px-4"
>
    {#each Models as Model,key}
        <ModelsCard {Model} {key} />
    {/each}
</div>
