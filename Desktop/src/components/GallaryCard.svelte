

<script>
    import EditVideoModal from './EditVideoModal.svelte';

    let imgSource ='C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Temp/poster.png';
    let showEditModal = false;

    function openEditModal() {
        showEditModal = true;
    }

    function handleCancel() {
        showEditModal = false;
    }

    function handleEditSave() {
        // Logic to save the edited video length
        showEditModal = false;
    }
</script>

<div class="gallery-card">
    <img  
    src={imgSource} alt="video preview"/>
   
    <div class="details">
        <p class="details-link"> Details here...</p>
    </div>
    <div class="buttons">

        <button class="edit" on:click={openEditModal}>Edit  </button>
        {#if showEditModal}
            <EditVideoModal on:cancel={handleCancel} on:save={handleEditSave} />
        {/if}

        <button class="process">Process</button>
        <button class="download">Download</button>
        <button class="delete">Delete </button>
    </div>
</div>



  <style>
    .gallery-card {
        border: 2px solid #007bff;
        border-radius: 4px;
        padding: 8px;
        width: 200px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin: 8px;
    }
    .gallery-card img {
        width: 100%;
        border-radius: 4px;
    }
    .gallery-card .details {
        margin: 4px 0;
    }
    .gallery-card .details   p{
            font-size: 10px;
        }
    .gallery-card .length {
        font-size: 10px;
        color: #555;
    }
    .gallery-card .buttons {
        display: flex;
        justify-content: space-between;
    }
    .gallery-card .buttons button {
        background-color: #007bff;
        color: #fff;
        border: none;
        padding: 4px 6px;
        border-radius: 2px;
        cursor: pointer;
        font-size: 8px;
    }
    .gallery-card .buttons button.delete {
        background-color: #dc3545;
    }
</style>