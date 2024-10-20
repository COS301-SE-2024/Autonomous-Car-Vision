<script>
    import { createEventDispatcher } from "svelte";
    import { TextField, Icon } from "svelte-materialify";
    import {mdiAccountPlus} from "@mdi/js";
    import axios from "axios";
    import { onMount } from "svelte";
    import {theme} from '../stores/themeStore';
  
   let email = ''; 
   let newMembers = []; 

    let HOST_IP;
   onMount(async () => {
    HOST_IP = await window.electronAPI.getHostIp();
   });
   
   function addMemberToList() {
        if (email.trim()) {
        newMembers = [...newMembers, email.trim()]; // Add the email to the array
        email = ''; // Clear the email field
        }
    }

    const dispatch = createEventDispatcher();
  
    function closePopup() {
        dispatch("cancel");
    }

    function addMember() {
        sendEmails();
        dispatch("save", { members: newMembers });
    }

    const sendEmails = async () => {
        // Send the emails to the new members
        try {
            const response = await axios.post("http://" + HOST_IP + ":8000/sendInviteEmail/", {
                newMembers: newMembers,
                teamName: window.electronAPI.getTeamName(),
            });
        } catch (error) {
            console.error("Sending invites failed:", error);
        }
    };
  
  </script>

  
{#if $theme === 'highVizLight'}
<div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
  <div
    class="bg-theme-dark-background p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
  >
  <div id="form" class="flex flex-col gap-2 py-3 text-black">
    <TextField 
        bind:value={email}
        outlined 
        class="border-b border-dark-primary text-white">Email address

         <!-- svelte-ignore a11y-click-events-have-key-events -->
         <div
         slot="append"
         on:click={addMemberToList}
       >
         <Icon path={mdiAccountPlus} class="cursor-pointer"/>
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
          class="font-medium bg-opacity-70 px-4 py-2 bg-highVizLight-error text-white rounded hover:bg-opacity-100 transition-all duration-300 ease-in-out"
          >Cancel</button
        >
        <button
          on:click={addMember}
          class="font-medium bg-opacity-70 px-4 py-2 bg-highVizLight-secondary text-white rounded hover:bg-opacity-100 transition-all duration-300 ease-in-out"
          >Add</button
        >
      </div>
    </div>
  </div>
{:else}
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
{/if}
 
  