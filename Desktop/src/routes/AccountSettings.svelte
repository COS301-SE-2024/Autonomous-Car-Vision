<script>
    import { TextField, Button, Avatar, Icon } from "svelte-materialify";
    import { onMount } from "svelte";
    import { mdiAccount } from "@mdi/js/mdi";
  
    let username = "";
    let email = "";
  
    let profilePicture = "";
  
    function updateProfilePicture() {
      // Function to handle profile picture update
    }
  
    function changePassword() {
      // Function to handle password change
    }
  
    function saveChanges() {
      // Function to handle saving other changes (username, email)
      alert("Changes saved!");
    }
  
    onMount(() => {
      const firstInput = document.querySelector("#username");
      if (firstInput) {
        firstInput.focus();
      }
    });
  </script>
  
  <div class="flex flex-col items-center justify-center min-h-screen">
    <div
      class="flex flex-col items-center justify-center p-8 rounded-lg shadow-lg w-96 border border-gray-dark space-y-3"
    >
      <h2 class="text-2xl font-bold mb-4 text-center text-black">
        Account Settings
      </h2>
  
      <!-- Profile Picture -->
      <div class="flex flex-col items-center mb-4 space-y-3">
        {#if profilePicture != ""}
          <Avatar size="15rem">
              <img src={profilePicture} alt="Avatar" />
          </Avatar>
        {:else}
          <Avatar size="15rem" class="bg-gray">
            <Icon path={mdiAccount} />
          </Avatar>
        {/if}
        <Button
          class="shadow-none text-blue text-transform-none"
          on:click={updateProfilePicture}>Edit</Button
        >
      </div>
  
      <!-- Edit Username -->
      <div class="mb-4">
        <label for="username" class="block text-green mb-1">Username</label>
        <TextField
          id="username"
          bind:value={username}
          class="w-full p-2 border border-green rounded red-text"
        />
      </div>
  
      <!-- Edit Email -->
      <div class="mb-4 text-black">
        <label for="email" class="block text-green mb-1">Email</label>
        <TextField
          id="email"
          type="email"
          bind:value={email}
          class="w-full p-2 border border-green rounded"
        />
      </div>
  
      <Button class="shadow-none rounded" on:click={changePassword}
        >Change Password?</Button
      >
  
      <!-- Save Changes -->
      <Button class="bg-green rounded" on:click={saveChanges}>Save Changes</Button
      >
    </div>
  </div>
  
  <style>
  </style>
  