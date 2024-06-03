<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let videoSource="https://sveltejs.github.io/assets/caminandes-llamigos.mp4";

    // let imgSource= "https://sveltejs.github.io/assets/caminandes-llamigos.mp4";
    function save() {
        dispatch('save');
    }
</script>


<div class="overlay mx-autorounded-xl bg-gray"></div>
<div class="mx-autorounded-lg bg-gray-dark">
    <video class="video-preview" src={videoSource} controls>
        <track kind="captions">
    </video>
    <div class="buttons">
         <button on:click={save} class="save text-gray-light text-bold">Done </button>
    </div>
</div>


<style>
    /* .modal {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border: 1px solid #ccc;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    } */

    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
    }

    .buttons {
        margin-top: 20px;
    }

    .buttons  button {
        margin: 0 10px;
        color: #fff;
        border: none;
        padding: 8px 12px;
        border-radius: 2px;
        cursor: pointer;
        font-size: 10px;
    }

    .video-preview {
        width: 100%;
        height: auto;
    }

    /* .timeline {
        margin-top: 10px;
        width: 100%;
    } */
</style>