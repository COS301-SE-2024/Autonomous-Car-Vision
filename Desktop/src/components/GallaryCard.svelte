

<script>
    
    import GallaryMore from './GallaryMore.svelte';

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

    function handleBack() {
            // Logic for the back button
            showMoreModal = false;
        }
   
</script>

<div class="gallery-card">
    <div class="image-container">
            <img  
            src={imgSource} alt="video preview"/>
            <div class="button-container">
                {#if isDownloaded}
                    <button class="more"  on:click={handleMore}>More</button>      
                {:else}
                    <button class="download" on:click={handleDownload}>Download</button>
                {/if}
            </div>
    </div>
    
    <div class="details">
        <p class="details-link"> Details here...</p>
    </div>
    <div>
        {#if showMoreModal}
          <GallaryMore on:close={handleBack}/>
         {/if}
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
   
    .details {
        padding: 10px;
        background-color: #f9f9f9;
        border-top: 1px solid #ccc;
    }
</style>