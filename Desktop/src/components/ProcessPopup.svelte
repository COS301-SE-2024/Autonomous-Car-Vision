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
    class="fixed inset-0 flex items-center justify-center bg-modal z-50"
>
    <div
        class="bg-white p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
    >
        <div class="flex flex-col boder border-theme-dark-backgroundBlue">
            <p class="text-md">Are you sure you want to process this video?</p>
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
