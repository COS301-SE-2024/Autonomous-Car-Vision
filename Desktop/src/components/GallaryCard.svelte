

<script>
    
    import GallaryMore from './GallaryCard.svelte';

    let showMoreModal = false;
    let imgSource ='C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Temp/poster.png';
    let isDownloaded = true;

    function handleDownload() {
        // Logic to download the video
        isDownloaded = true;
    }

    function handleMore() {
        // Logic for the more button
       showMoreModal = true;
    
    }
   
</script>

<div class="gallery-card">
    <div class="image-container">
            <img  
            src={imgSource} alt="video preview"/>
            <div class="button-container">
                {#if isDownloaded}
                    <button class="more" on:click={handleMore}>More</button>    
                    {#if showMoreModal}
                        <GallaryMore/>
                    {/if}
                {:else}
                    <button class="download" on:click={handleDownload}>Download</button>
                {/if}
            </div>
        <!-- <div class="button-cluster">
            <button class="edit" on:click={openEditModal} >Edit</button>
                {#if showEditModal}
                    <EditVideoModal on:cancel={handleCancel} on:save={handleEditSave} />
                {/if}
            <button class="process">Process</button>
            <button class="download">Download</button>
            <button class="delete">Delete</button>
        </div> -->
    </div>
    
    <div class="details">
        <p class="details-link"> Details here...</p>
    </div>
</div>



  <style>
    .gallery-card {
        position: relative;
        overflow: hidden;
        border: 2px solid #007bff;
        border-radius: 4px;
        padding: 8px;
        width: 200px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin: 8px;
        transition: all 0.3s ease;
    }
     .img-container {
        
        position: relative;
    }

   .img-container img{
        width: 100%;
        border-radius: 4px;
        transition: filter 0.3s ease;
    }

     .image-container:hover img{
        filter: grayscale(100%);
    }

    .button-container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -150%); 
        display: none; 
    }

    .gallery-card:hover .button-container {
        display: block;
    }

    .button-container button {
        cursor: pointer;
        background-color: #007bff;
        color: #fff;
        border: none;
        padding: 4px 6px;
        border-radius: 2px;
        font-size: 8px;
    }
    /*
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
   

    .button-cluster {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 0, 0, 0.5);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .image-container:hover .button-cluster {
        opacity: 1;
    }

    .button-cluster button {
        margin: 0 5px;
        padding: 4px 6px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background-color: #007bff;
        color: #fff;
        border-radius: 2px;
        font-size: 8px;
    }
    .button-cluster button.delete {
        background-color: #dc3545;
    } */
    .details {
        padding: 10px;
        background-color: #f9f9f9;
        border-top: 1px solid #ccc;
    }
</style>