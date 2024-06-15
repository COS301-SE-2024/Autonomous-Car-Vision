

<script> 
import { createEventDispatcher } from 'svelte';
import TimelineModal from './TimelineModal';

const dispatch = createEventDispatcher();

// Placeholder list of models with profile images
let models = [
    { id: 1, name: 'Mod.1', profileImg: 'https://placekitten.com/300/300',TimeStamp: 'Jul 8, 2015' , Version: 1.4},
    { id: 2, name: 'Mod.2', profileImg: 'https://placekitten.com/300/300',TimeStamp: 'Aug 8, 2015' , Version: 1.4 },
    { id: 3, name: 'Mod.3', profileImg: 'https://placekitten.com/300/300',TimeStamp: 'May 8, 2015' , Version: 1.8 },
    { id: 4, name: 'Mod.4', profileImg: 'https://placekitten.com/300/300',TimeStamp: 'Jun 10, 2024' , Version: 2.6},
    { id: 5, name: 'Mod.5', profileImg: 'https://placekitten.com/300/300',TimeStamp: 'Jun 8, 2015' , Version: 1.4},
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
        <p class="text-xs">{model.name}</p>
        <p class="text-xs">{model.TimeStamp}</p>
        <p class="text-xs">{model.Version}</p>
    </div>
{/each}
</div>  
