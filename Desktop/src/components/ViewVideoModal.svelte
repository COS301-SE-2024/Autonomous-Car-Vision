<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let videoSource="https://sveltejs.github.io/assets/caminandes-llamigos.mp4";
    function save() {
        dispatch('save');
    }
</script>


<div class="overlay mx-autorounded-xl bg-gray"></div>
<div class="mx-autorounded-lg bg-theme-dark-background ">
    <video class="video-preview" src={videoSource} controls>
        <track kind="captions">
    </video>
    <div class="buttons">
         <button on:click={save} class="save text-theme-dark-white bg-theme-dark-background  text-bold">Done </button>
    </div>
</div>


<style>

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
</style>