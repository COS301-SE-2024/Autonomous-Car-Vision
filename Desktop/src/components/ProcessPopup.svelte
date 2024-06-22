<script>
    import { push } from "svelte-spa-router";
    import { createEventDispatcher } from "svelte";

    export let showProcessPopup;

    const dispatch = createEventDispatcher();

    function closePopup() {
        dispatch("closePopup");
    }

    function processVideo() {
        dispatch("processVideo");
        console.log("Processing video", showProcessPopup);
    }
</script>

<div
    class="fixed inset-0 flex items-center justify-center bg-theme-dark-background bg-opacity-50 z-50"
>
    <div
        class="bg-white p-6 rounded-lg shadow-lg border border-theme-keith-primary"
    >
        <div class="flex flex-col p-8 boder-1 border-theme-dark-backgroundBlue">
            <h1>Are you sure you want to process this video?</h1>
            <div class="flex mt-4 space-x-4 justify-start">
                <button
                    class="bg-theme-dark-primary px-4 py-2 text-white rounded"
                    on:click={processVideo}>Yes</button
                >
                <button
                    class="bg-theme-dark-error text-white px-4 py-2 rounded"
                    on:click={closePopup}>No</button
                >
            </div>
        </div>
    </div>
</div>
