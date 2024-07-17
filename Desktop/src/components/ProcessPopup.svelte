<script>
    import { push } from "svelte-spa-router";
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";

    import { isLoading } from "../stores/loading";

    export let showProcessPopup;
    export let models = [];
    export let selectedModelName;

    const dispatch = createEventDispatcher();

    function closePopup() {
        dispatch("closePopup");
    }

    function processVideo() {
        isLoading.set(true);
        dispatch("processVideo", { modelName: selectedModelName});
        console.log("Processing video", showProcessPopup);
    }

    function handleModelChange(event) {
        selectedModelName = event.target.value;
    }
</script>

<div
    class="fixed inset-0 flex items-center justify-center bg-modal z-50"
>
    <div
        class="bg-theme-dark-background p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
    >
        <div class="flex flex-col boder border-theme-dark-backgroundBlue">
            <p class="text-md">Are you sure you want to process this video? Please select a model to process below.</p>
            <select on:change={handleModelChange} bind:value={selectedModelName} class="mt-2 p-2 border rounded bg-theme-dark-primary text-white">
                {#each models as model}
                    <option value={model.model_name}>{model.model_name}</option>
                {/each} ▼ 
            </select>
            <div class="flex mt-4 space-x-4 justify-start">
                <button
                class="bg-theme-dark-error font-medium text-white px-4 py-2 rounded"
                on:click={closePopup}>No</button
                >
                <button
                    class="bg-theme-dark-primary font-medium px-4 py-2 text-white rounded"
                    on:click={processVideo}>Yes</button
                >
            </div>
        </div>
    </div>
</div>
