<script>
    import { createEventDispatcher } from "svelte";
    import { Button, TextField, Icon } from "svelte-materialify";
    import {mdiAccountPlus} from "@mdi/js";
  
   let email = ''; 
   let newMembers = []; 
   
   function addMemberToList() {
        if (email.trim()) {
        newMembers = [...newMembers, email.trim()]; // Add the email to the array
        email = ''; // Clear the email field
        }
    }

    const dispatch = createEventDispatcher();
  
    function closePopup() {
    dispatch("closePopup");
  }

    function addMember() {
      console.log("addMember called");
    }
  
  </script>
  
  <div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
    <div
      class="bg-theme-dark-background p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
    >
    <div id="form" class="flex flex-col gap-2 py-3 text-white">
      <TextField 
          bind:value={email}
          outlined 
          class="border-b border-dark-primary ">Email address

           <!-- svelte-ignore a11y-click-events-have-key-events -->
           <div
           slot="append"
           on:click={addMemberToList}
         >
           <Icon path={mdiAccountPlus} class="text-theme-dark-primary cursor-pointer"/>
         </div>
      </TextField>
    </div>
    <div class="flex gap-2 newMember content-fit">
      {#each newMembers as member}
          <p class="bg-theme-dark-primary rounded-lg px-1 mt-2 text-theme-dark-white hoverClass">{member}</p>
       {/each}
    </div> 
        <div class="flex mt-4 space-x-4">
          <button
            on:click={closePopup}
            class="font-medium px-4 py-2 bg-theme-dark-error text-white rounded"
            >Cancel</button
          >
          <button
            on:click={addMember}
            class="font-medium px-4 py-2 bg-theme-dark-primary text-white rounded"
            >Add</button
          >
        </div>
      </div>
    </div>
  