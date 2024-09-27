<script>
  import {
    TextField,
    Button,
    Avatar,
    MaterialAppMin,
    Icon,
    Tooltip,
  } from "svelte-materialify";
  import { onMount } from "svelte";
  import axios from "axios";
  import { mdiAccount, mdiImageEdit } from "@mdi/js/mdi";
  import { push } from "svelte-spa-router";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import toast, { Toaster } from "svelte-french-toast";

  // Loading screen Imports
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";
  import CryptoJS from "crypto-js";

  let user = {
    username: "",
    email: "",
    profile_picture: "https://media.contentapi.ea.com/content/dam/ea/f1/f1-23/common/articles/patch-note-v109/pj-f123-bel-w01-rus.jpg.adapt.1456w.jpg", // Test Image "images/HighViz.png"
  };
  let isHovered = false; // To track hover state
  let fileInput; // For referencing the file input element

  const handleHover = () => {
    isHovered = true;
  };

  const handleMouseLeave = () => {
    isHovered = false;
  };

  const updateProfilePicture = () => {
    // Trigger file input click
    fileInput.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0]; // Get the first selected file
    if (file) {
      const reader = new FileReader();

      // Load the selected image and update user.profile_picture
      reader.onload = (e) => {
        user.profile_picture = e.target.result;
      };

      reader.readAsDataURL(file); // Read the file as a data URL (base64)
    }
  };

  function changePassword() {
    push("/changePassword");
  }

  const saveChanges = async () => {
    // Function to handle saving other changes (username, email)
    console.log("Username: " + user.username);
    console.log("email: " + user.email);
    console.log("Profile: " + user.profile_picture);

    // Save the changes to the database

    console.log(window.electronAPI.getToken());

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/changeUserDetails/",
        {
          uid: window.electronAPI.getUid(),
          uname: user.username,
          uemail: user.email,
          token: window.electronAPI.getToken(),
        },
      );

      console.log("token" + window.electronAPI.getToken());

      if (response.data.status == "200") {
        toast.success("Changes saved successfully!", {
          duration: 5000,
          position: "top-center",
        });

        window.electronAPI.storeUname(user.username);
        window.electronAPI.storeUemail(user.email);
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
    }, 2000);

    // Fetch user data
    axios
      .post("http://localhost:8000/getUserData/", {
        uid: window.electronAPI.getUid(),
      })
      .then((response) => {
        user.username = response.data.uname;
        user.email = response.data.uemail;
        let profileEmail = response.data.uemail;
        profileEmail = profileEmail.trim().toLowerCase();
        const emailHash = CryptoJS.SHA256(profileEmail);
        user.profile_picture = `https://www.gravatar.com/avatar/${emailHash}?d=retro`;
        console.log(user.profile_picture);
      })
      .catch((error) => {
        console.error("Failed to fetch user data:", error);
        toast.error("Failed to fetch user data", {
          duration: 5000,
          position: "top-center",
        });
      });
  });
</script>

<MaterialAppMin theme={"dark"}>
  <ProtectedRoutes>
    {#if $isLoading}
      <div class="flex justify-center">
        <Spinner />
      </div>
    {:else}
      <Toaster />
      <div
        class="flex text-white flex-col items-center justify-center min-h-screen shadow-lg background-card"
      >
        <div
          class="flex flex-col items-center justify-center p-4 shadow rounded-lg w-1/2 max-w-md border space-y-3"
        >
          <h2 class="text-2xl font-bold mb-4 text-center">Account Settings</h2>

          <!-- Profile Picture -->
          <div
            class="flex flex-col items-center mb-4 space-y-3 rounded-full border avatar-image"
            on:mouseenter={handleHover}
            on:mouseleave={handleMouseLeave}
          >
            {#if user.profile_picture != ""}
              <Avatar size="15rem">
                <img
                  src={user.profile_picture}
                  alt="Avatar"
                  class="avatar-image"
                />
                {#if isHovered}
                  <!-- svelte-ignore a11y-click-events-have-key-events -->
                  <div
                    class="absolute text-dark-primary p-2 cursor-pointer pencil-icon"
                    on:click={updateProfilePicture}
                  >
                    <Icon path={mdiImageEdit} size="2rem" />
                  </div>
                {/if}
              </Avatar>
            {:else}
              <Avatar size="15rem" class="bg-theme-keith-jet">
                <Icon path={mdiAccount} class="avatar-image" />
                {#if isHovered}
                  <!-- svelte-ignore a11y-click-events-have-key-events -->
                  <div
                    class="absolute text-dark-primary p-2 cursor-pointer pencil-icon"
                    on:click={updateProfilePicture}
                  >
                    <Icon path={mdiImageEdit} size="2rem" />
                  </div>
                {/if}
              </Avatar>
            {/if}
          </div>
          <!-- Hidden file input for image selection -->
          <input
            type="file"
            accept="image/*"
            containerStyles="border-color: #8492a6; color: black"
            style="display:none;"
            bind:this={fileInput}
            on:change={handleFileChange}
          />

          <!-- Edit Username -->
          <div class="mb-2 w-1/2">
            <TextField
              bind:value={user.username}
              placeholder={user.username}
              outlined
              dense
              id="username">Username</TextField
            >
          </div>

          <!-- Edit Email -->
          <div class="mb-2 w-1/2">
            <TextField
              bind:value={user.email}
              placeholder={user.email}
              outlined
              dense
              id="email"
              type="email">Email</TextField
            >
          </div>

          <Button class="shadow-none rounded" on:click={changePassword}
            >Change Password?</Button
          >

          <!-- Save Changes -->
          <Button
            class="bg-theme-dark-backgroundBlue text-theme-dark-white rounded"
            on:click={saveChanges}>Save Changes</Button
          >
        </div>
      </div>
    {/if}
  </ProtectedRoutes>
</MaterialAppMin>

<style>
  /* Add smooth transition for opacity change */
  .avatar-image {
    opacity: 1;
  }

  /* Reduce opacity to 60% when hovered */
  .avatar-image:hover {
    opacity: 0.6;
    transition: opacity 0.3s ease;
  }

  /* Pencil icon styling */
  .pencil-icon svg {
    color: var(--theme-dark-white); /* Icon color */
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
