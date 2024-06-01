<script>
    import { writable } from 'svelte/store';
    import EditVideoModal from './EditVideoModal.svelte';
    import DeleteModal from './DeleteModal.svelte';
    import ModelList from './ModelList.svelte';
    import ViewVideoModal from './ViewVideoModal.svelte';
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    const currentTab = writable('original');
    const showModelList = writable(false);
    let selectedModel = null;
    
    let imgSource ='C:/Users/NTOLO LOGISTICS/OneDrive/Documents/GitHub/Autonomous-Car-Vision/Documentation/Images/Temp/poster.png';
    let showEditModal = false;
    let showViewModal = false;
    let showDeleteModal = false;

    function back() {
        // const event = new CustomEvent('close');
        // dispatchEvent(event);
        dispatch('close');
    }

    function switchTab(tab) {
        currentTab.set(tab);
    }

    function edit() {
        // Edit functionality
        showEditModal = true;
    }

    function process() {
        // Process functionality
    }

    function reProcess()
    {
        //re-process functionality
    }

    function deleteItem() {
        // Delete functionality
        showDeleteModal = true;
    }

    function model() {
        // Model functionality
    }

    function handleCancel() {
        showEditModal = false;
        showDeleteModal = false;
    }

    function handleEditSave() {
        // Logic to save the edited video length
        showEditModal = false;
    }

    function handleDeleteSave() {
        // Logic to delete the video
        showDeleteModal = false;
    }

    function toggleModelList() {
        showModelList.update(value => !value);
    }

    function handleModelSelect(event) {
        selectedModel = event.detail;
        showModelList.set(false);
    }

    function toggleViewModal(){
        showViewModal = true;
    }

    function handleViewDone()
    {
        showViewModal = false;
    }

</script>

<div class="modal">
    <div>
        <button  class="back-button bg-green-600" on:click={back}>Back</button>
    </div>
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
            <p>Details here</p>
        </div>
        <div class="button-cluster">
            <button on:click={edit} >Edit</button>
                {#if showEditModal}
                    <EditVideoModal on:cancel={handleCancel} on:save={handleEditSave} />
                {/if}
            <button on:click={process}>Process</button>
            <button on:click={deleteItem}>Delete</button>
                {#if showDeleteModal}
                    <DeleteModal on:cancel={handleCancel} on:save={handleDeleteSave} />
                {/if}
            <div class="model-button">
                <button class="model" on:click={toggleModelList}>
                    {#if selectedModel}
                         <img src={selectedModel.profileImg}  class="profile-image" alt="Selected Model" width="20" height="20"/> 
                    {:else}
                         <img src={imgSource} class="profile-image" alt="default Model" width="20" height="20"/>
                    {/if}
                </button>
                {#if $showModelList}
                    <ModelList on:select={handleModelSelect} />
                {/if}
            </div>
            
        </div>
    </div>

    <div class="content { $currentTab === 'processed' ? 'active' : '' }">
        <!-- Processed tab content goes here -->

        <div class="image-container">
            <img  
            src={imgSource} alt="video thumbnail"/>
        </div>
        <div class="details">
            <p>Details here</p>
        </div>
        <div class="button-cluster">
            <button on:click={toggleViewModal} >View</button>
                {#if showViewModal}
                  <ViewVideoModal on:save={handleViewDone} />   <!-- on:play={handleControl}  -->
                {/if}
            <button on:click={reProcess}>Re-Process</button>
        </div>
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

    .back-button  {
        margin: 0 10px;
        color: #fff;
        border: none;
        padding: 8px 12px;
        border-radius: 2px;
        cursor: pointer;
        font-size: 10px;
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
        margin: auto;
    }

    
    .button-cluster {
        margin-top: 10px;
        display: flex;
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

    
    .button-cluster .model {
        margin: 2px;
        padding: 5px;
        background-color: #4b8dd3;
        border: none;
        color: white;
        cursor: pointer;
        width: 20%;
        height: 80%;
        position: relative;
        
    }

    
    .profile-image {
        position: relative;
        width: 50%;
        margin:auto;
        border-radius: 50%;
    }

    /* .model-button {
        position: relative;
    } */

    .details {
        padding: 10px;
        background-color: #f9f9f9;
        border-top: 1px solid #ccc;
        margin-top: 10px;
    }
</style>
