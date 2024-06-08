<script>
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
            img: 'https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
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
    class="grid grid-cols-2 gap-6 h-screen py-4 px-4"
>
    {#each Models as Model,key}
        <ModelsCard {Model} {key} />
    {/each}
</div>
