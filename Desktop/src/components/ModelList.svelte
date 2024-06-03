<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    // Placeholder list of models with profile images
    let models = [
        { id: 1, label: 'Mod.1', profileImg: 'https://placekitten.com/300/300' },
        { id: 2, label: 'Mod.2', profileImg: 'https://placekitten.com/300/300' },
        { id: 3, label: 'Mod.3', profileImg: 'https://placekitten.com/300/300' },
        { id: 4, label: 'Mod.4', profileImg: 'https://placekitten.com/300/300' },
        { id: 5, label: 'Mod.5', profileImg: 'https://placekitten.com/300/300' },
    ];

    function selectModel(model) {
        dispatch('select', model);
    }
</script>

<div class="absolute top-0 right-0 bg-theme-keith-primary border border-gray-300 shadow-lg p-4 z-50 flex flex-col rounded-lg">
    {#each models as model}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div class="mb-2 cursor-pointer flex items-center border-b border-theme-keith-accenttwo" on:click={() => selectModel(model)}>
            <img src={model.profileImg} alt="Model Profile" class="w-12 h-12 rounded-full mr-2">
            <p class="text-xs">{model.label}</p>
        </div>
    {/each}
</div>