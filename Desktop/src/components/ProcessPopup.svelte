<script>
    export let showProcessPopup;

    let dialog; // HTMLDialogElement

    $: if (dialog && showProcessPopup) dialog.showModal();

    function close() {
        dialog.close();
        showProcessPopup = false;
    }
</script>

<dialog
    class="slot"
    bind:this={dialog}
    on:close={() => (showProcessPopup = false)}
    on:click|self={() => dialog.close()}
    on:keypress
>
    <div class="flex flex-col p-8">
        <button class="bg-black text-white text-center rounded-xl flex justify-center w-3/12 cursor-pointer" on:click={close}>
            <p class="text-center">
                Close
            </p>
        </button>
        <slot name="body" />
    </div>
</dialog>

<style>
    .slot {
        position: relative;
        top: 50%;
        margin-right: auto;
        margin-left: auto;
        border-radius: 20px;
    }

    button:hover {
        cursor: pointer;
    }

    dialog {
        max-width: 32em;
        border-radius: 0.2em;
        border: none;
        padding: 0;
    }
    dialog::backdrop {
        background: rgba(0, 0, 0, 0.3);
    }
    dialog[open] {
        animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes zoom {
        from {
            transform: scale(0.95);
        }
        to {
            transform: scale(1);
        }
    }
    dialog[open]::backdrop {
        animation: fade 0.2s ease-out;
    }
    @keyframes fade {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
</style>
