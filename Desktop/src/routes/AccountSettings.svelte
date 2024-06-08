<script>
  import { TextField, Button, Avatar, Icon } from "svelte-materialify";
  import { onMount } from "svelte";
  import axios from "axios";
  import { mdiAccount } from "@mdi/js/mdi";
  import { push } from "svelte-spa-router";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";

  let username = "";
  let email = "";
  let profilePicture = "";
  let notification = "";
  let notificationType = "";

  function updateProfilePicture() {
    // Function to handle profile picture update
  }

  function changePassword() {
    push("/changePassword");
  }

  const saveChanges = async () => {
    // Function to handle saving other changes (username, email)
    console.log("Username: " + username);
    console.log("email: " + email);
    console.log("Profile:");

    // Save the changes to the database

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/changeUserDetails/",
        {
          uid: localStorage.getItem("uid"),
          uname: username,
          uemail: email,
          token: localStorage.getItem("token"),
        }
      );

      if (response.data.status == "200") {
        notification = "Changes saved successfully!";
        notificationType = "success";
      } else {
        notification = "Failed to save changes!";
        notificationType = "error";
      }
    } catch (error) {
      console.error("Failed to save changes:", error);
    }
  };

  onMount(() => {
    const firstInput = document.querySelector("#username");
    if (firstInput) {
      firstInput.focus();
    }
  });
</script>

<ProtectedRoutes>
<div class="flex flex-col items-center justify-center min-h-screen">
  <div
    class="flex flex-col items-center justify-center p-8 rounded-lg shadow-lg w-96 border border-theme-keith-accentont space-y-3"
  >
    <h2 class="text-2xl font-bold mb-4 text-center">Account Settings</h2>

    <!-- Profile Picture -->
    <div class="flex flex-col items-center mb-4 space-y-3">
      {#if profilePicture != ""}
        <Avatar size="15rem">
          <img src={profilePicture} alt="Avatar" />
        </Avatar>
      {:else}
        <Avatar size="15rem" class="bg-theme-keith-jet">
          <Icon path={mdiAccount} />
        </Avatar>
      {/if}
      <Button
        class="shadow-none text-theme-keith-secondary text-transform-none"
        on:click={updateProfilePicture}>Edit</Button
      >
    </div>

    <!-- Edit Username -->
    <div class="mb-4">
      <label for="username" class="block text-theme-keith-secondary mb-1"
        >Username</label
      >
      <TextField
        id="username"
        bind:value={username}
        class="text-black-important w-full p-2 border border-theme-keith-accenttwo rounded text-black-important"
      />
    </div>

    <!-- Edit Email -->
    <div class="mb-4 text-black">
      <label for="email" class="block text-theme-keith-secondary mb-1"
        >Email</label
      >
      <TextField
        id="email"
        type="email"
        bind:value={email}
        class="text-black-important w-full p-2 border border-theme-keith-accenttwo rounded"
      />
    </div>

    <Button class="shadow-none rounded" on:click={changePassword}
      >Change Password?</Button
    >

    <!-- Save Changes -->
    <Button class="bg-theme-keith-accentone rounded" on:click={saveChanges}
      >Save Changes</Button
    >
  </div>

  {#if notification}
    <div class={`notification ${notificationType}`}>
      {notification}
    </div>
  {/if}
</div>
</ProtectedRoutes>


<style>
  .text-black-important {
    color: black !important;
  }
  .notification {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 1rem 2rem;
    border-radius: 5px;
    color: white;
    font-weight: bold;
  }
  .notification.success {
    background-color: green;
  }
  .notification.error {
    background-color: red;
  }
</style>
