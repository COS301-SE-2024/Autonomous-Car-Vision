<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let imgSource= "C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Temp/poster.png";


    function save() {
        dispatch('save');
    }
</script>


<div class="overlay mx-autorounded-xl rounded-lg"></div>
<div class="modal mx-autorounded-lg">
    <!-- <video class="video-preview" src={videoSrc} controls></video> -->
     <img src={imgSource} alt="video preview"/>
    <input type="range" min="0" max="100" class="timeline" /> <!--edt this please-->
    <div class="buttons">
        <button class="cancel bg-blue-600" >Pause/Play</button>  <!-- on:click={cancel} -->
         <button on:click={save} class="save bg-green-600">Done </button> <!--on:click={save} -->
    </div>
</div>


<style>
    .modal {
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
    }

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

    .timeline {
        margin-top: 10px;
        width: 100%;
    }
</style>