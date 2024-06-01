<script>
    import { writable } from 'svelte/store';

    const currentTab = writable('original');
    
    let imgSource ='C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Temp/poster.png';

    function switchTab(tab) {
        currentTab.set(tab);
    }

    function edit() {
        // Edit functionality
    }

    function process() {
        // Process functionality
    }

    function deleteItem() {
        // Delete functionality
    }

    function model() {
        // Model functionality
    }
</script>

<div class="modal">
    <div class="tabs">
        <div class="tab { $currentTab === 'original' ? 'active' : '' }" on:click={() => switchTab('original')}>Original</div>
        <div class="tab { $currentTab === 'processed' ? 'active' : '' }" on:click={() => switchTab('processed')}>Processed</div>
    </div>
    
    <div class="content { $currentTab === 'original' ? 'active' : '' }">
        <div class="image-container">
            <img  
            src={imgSource} alt="video thumbnail"/>
        </div>
        <div class="details">
            <p>Video Title</p>
            <p>Length: 3:45</p>
        </div>
        <div class="button-cluster">
            <button on:click={edit}>Edit</button>
            <button on:click={process}>Process</button>
            <button on:click={deleteItem}>Delete</button>
            <button class="model" on:click={model}><div class="profile-image">
                <img  
                src={imgSource} alt="model profile"/>
            </div></button>
        </div>
    </div>

    <div class="content { $currentTab === 'processed' ? 'active' : '' }">
        <!-- Processed tab content goes here -->
        <p>Processed content will be displayed here.</p>
    </div>
</div>


<style>
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgb(252, 252, 252);
        padding: 20px;
        border: 1px solid #ccc;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        width: 80%;
        /* max-width: 800px; */
        border-radius: 8px;
    }

    .tabs {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #ccc;
        margin-bottom: 20px;
    }

    .tab {
        padding: 10px 20px;
        cursor: pointer;
    }

    .tab.active {
        border-bottom: 2px solid #007BFF;
        font-weight: bold;
    }

    .content {
        display: none; 
    }

    .content.active {
        display: block;
    }

    .image-container {
        position: relative;

    }

    .image-container img {
        position: relative;
        width: 50%;
    }

    .profile-image {
        position: relative;
        width: 10%;
    }

    .profile-image img {
        position: center;
        width: 100%;
        border-radius: 100%;
    }
    .button-cluster {
        margin-top: 10px;
    }

    .button-cluster button {
        margin: 5px;
        padding: 10px;
        background-color: #007BFF;
        border: none;
        color: white;
        border-radius: 4px;
        cursor: pointer;
    }
    .button-cluster button.model {
        margin: 5px;
        padding: 10px;
        background-color: #4b8dd3;
        border: none;
        color: white;
        border-radius: 4px;
        cursor: pointer;
        /* width: 10%; */
    }

    .details {
        padding: 10px;
        background-color: #f9f9f9;
        border-top: 1px solid #ccc;
        margin-top: 10px;
    }
</style>
