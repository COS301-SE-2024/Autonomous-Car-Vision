<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let imgSource= "C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Temp/poster.png";

    function cancel() {
        dispatch('cancel');
    }

    function save() {
        dispatch('save');
    }
</script>

<div class="modal mx-autorounded-lg">
     <img src={imgSource} alt="video preview"/>
    <input type="range" min="0" max="100" class="timeline" />
    <div class="buttons">
        <button on:click={cancel} class="cancel bg-red-600" >Cancel</button>
         <button on:click={save} class="save bg-green-600">Save</button>
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