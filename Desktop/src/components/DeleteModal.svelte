<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function cancel() {
        dispatch('cancel');
    }

    function save() {
        dispatch('save');
    }
</script>


<div class="overlay mx-autorounded-xl rounded-lg"></div>
<div class="modal mx-autorounded-lg">
    <!-- <video class="video-preview" src={videoSrc} controls></video> -->
    <div class="timeline">
        <h3> Are you sure you would like to delete the video from your downloads?</h3>
        <br> 
        <p> You will have to re-download the video from the server to access it in future.</p>
    </div>
    
    <div class="buttons">
        <button on:click={cancel} class="cancel bg-pink-600" >Cancel</button>  <!-- on:click={cancel} -->
         <button on:click={save} class="save bg-red-600">Delete</button> <!--on:click={save} -->
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

    .timeline {
        margin-top: 10px;
        width: 100%;
    }

</style>