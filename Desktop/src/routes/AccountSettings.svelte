<script>
  import { TextField, Button, Avatar, Icon } from "svelte-materialify";
  import { onMount } from "svelte";
  import axios from "axios";
  import { mdiAccount, mdiImageEdit } from "@mdi/js/mdi";
  import { push } from "svelte-spa-router";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import toast, { Toaster } from "svelte-french-toast";

  // Loading screen Imports
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let username = "";
  let email = "";
  let profilePicture = "";
  let isHovered = false;   // To track hover state

  const handleHover = () => {
    isHovered = true;
  };

  const handleMouseLeave = () => {
    isHovered = false;
  };

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

    console.log(window.electronAPI.getToken());

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/changeUserDetails/",
        {
          uid: window.electronAPI.getUid(),
          uname: username,
          uemail: email,
          token: window.electronAPI.getToken(),
        }
      );

      console.log("token" + window.electronAPI.getToken());

      if (response.data.status == "200") {
        toast.success("Changes saved successfully!", {
          duration: 5000,
          position: "top-center",
        });

        window.electronAPI.storeUname(username);
        window.electronAPI.storeUemail(email);
      } else {
        toast.error("Failed to save changes", {
          duration: 5000,
          position: "top-center",
        });
      }
    } catch (error) {
      console.error("Failed to save changes:", error);
      toast.error("Failed to save changes", {
        duration: 5000,
        position: "top-center",
      });
    }
  };

  // For loading screen purposes
  onMount(() => {
    isLoading.set(true);
    const firstInput = document.querySelector("#username");
    if (firstInput) {
      firstInput.focus();
    }
    setTimeout(() => {
      isLoading.set(false);
    }, 4000);
  });
</script>

<ProtectedRoutes>
  {#if $isLoading}
    <div class="flex justify-center">
      <Spinner />
    </div>
  {:else}
    <Toaster />
    <div class="flex text-white flex-col items-center justify-center min-h-screen shadow-lg background-card">
      <div
        class="flex flex-col items-center justify-center p-4 shadow rounded-lg w-1/2 border space-y-3"
      >
        <h2 class="text-2xl font-bold mb-4 text-center">Account Settings</h2>

        <!-- Profile Picture -->
        <div class="cursor-pointer flex flex-col items-center mb-4 space-y-3 rounded-full border"  on:mouseenter={handleHover} on:mouseleave={handleMouseLeave}>
          {#if profilePicture != ""}
            <Avatar size="15rem">
              <img src={profilePicture} alt="Avatar" class="object-cover  avatar-image"/>
              {#if isHovered}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <div
                class="absolute text-black p-2 cursor-pointer pencil-icon"
                on:click={updateProfilePicture}>
                <Icon path={mdiImageEdit} size="2rem" />
              </div>
            {/if}
            </Avatar>
          {:else}
            <Avatar size="15rem" class="bg-theme-keith-jet">
              <Icon path={mdiAccount} class="object-cover  avatar-image"/>
                {#if isHovered}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <div
                class="absolute text-black p-2 cursor-pointer pencil-icon"
                on:click={updateProfilePicture}>
                <Icon path={mdiImageEdit} size="2rem" />
              </div>
            {/if}
            </Avatar>
          {/if}
        </div>

        <!-- Edit Username -->
        <div class="mb-4 w-1/2">
          <!-- <label for="username" class="block text-theme-keith-secondary mb-1"
            >Username</label
          > -->
          <TextField bind:value={username} outlined class="pt-4 border-b-2 border-dark-primary " id="username">Username</TextField>
         
        </div>

        <!-- Edit Email -->
        <div class="mb-4 w-1/2">
          <!-- <label for="email" class="block text-theme-keith-secondary mb-1"
            >Email</label
          > -->
          <TextField bind:value={email} outlined class="pt-4 border-b-2 border-dark-primary " id="email" type="email">Email</TextField>
        
        </div>

        <Button class="shadow-none rounded" on:click={changePassword}
          >Change Password?</Button
        >

        <!-- Save Changes -->
        <Button class="bg-theme-dark-backgroundBlue text-theme-dark-white rounded" on:click={saveChanges}
          >Save Changes</Button
        >
      </div>
    </div>
  {/if}
</ProtectedRoutes>


<style>
   /* Add smooth transition for opacity change */
   .avatar-image {
    transition: opacity 0.3s ease;
    opacity: 1;
  }

  /* Reduce opacity to 30% when hovered */
  .flex:hover .avatar-image {
    opacity: 0.3;
  }

  /* Pencil icon styling */
  .pencil-icon svg {
    color: #000; /* Icon color */
    background: white; /* Background for better visibility */
    border-radius: 50%;
    padding: 0.5rem;
    opacity: 1; /* Set icon opacity to 100% */
  }

  /* Ensure icon is always fully visible */
  .pencil-icon {
    opacity: 1;
  }
  </style>