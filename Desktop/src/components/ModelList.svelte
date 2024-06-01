<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    // Placeholder list of models with profile images
    let models = [
        { id: 1, label: 'Mod.1' ,profileImg: 'C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Donatello.png' },
        { id: 2, label: 'Mod.2' ,profileImg: 'C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Dawie.jpeg' },
        { id: 3, label: 'Mod.3' ,profileImg: 'C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Kea.png' },
        { id: 4, label: 'Mod.4' ,profileImg: 'C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/keith.jpg' },
        { id: 5, label: 'Mod.5' ,profileImg: 'C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Jordan.png' },
    ];

    function selectModel(model) {
        dispatch('select', model);
    }
</script>


<div class="model-list">
    {#each models as model}
        <div class="model-item" on:click={() => selectModel(model)}>
            <img src={model.profileImg} alt="Model Profile">
            <p style="font-size:8px;"> {model.label} </p>
        </div>
    {/each}
</div>

<style>
    .model-list {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 0;
        right: 5px;
        background-color: white;
        border: 1px solid #ccc;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        padding: 10px;
    }

    .model-item {
        margin-bottom: 10px;
        cursor: pointer;
    }

    .model-item img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
    }
</style>

