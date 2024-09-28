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
  import { mdiAccount, mdiLaunch } from "@mdi/js/mdi";
  import { push } from "svelte-spa-router";
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import toast, { Toaster } from "svelte-french-toast";
  import { theme } from "../stores/themeStore";

  // Loading screen Imports
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";
  import CryptoJS from "crypto-js";
  import { env } from '$env/dynamic/private';

  let themeMaterial = "dark";

  let HOST_IP;
  let user = {
    username: "",
    email: "",
    profile_picture: "https://media.contentapi.ea.com/content/dam/ea/f1/f1-23/common/articles/patch-note-v109/pj-f123-bel-w01-rus.jpg.adapt.1456w.jpg", // Test Image "images/HighViz.png"
  };

  const redirectToGravatar = () => {
    console.log("Redirecting to Gravatar...");
    window.open('https://en.gravatar.com/site/login', '_blank');
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
        "http://" + HOST_IP + ":8000/changeUserDetails/",
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
  onMount(async () => {
    isLoading.set(true);
     HOST_IP = await window.electronAPI.getHostIp();
    const firstInput = document.querySelector("#username");
    if (firstInput) {
      firstInput.focus();
    }
    setTimeout(() => {
      isLoading.set(false);
    }, 2000);

    // Fetch user data
    axios
      .post("http://" + HOST_IP + ":8000/getUserData/", {
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

  theme.subscribe((value) => {
    if(value == "highVizLight"){
      themeMaterial = "light"
    }else {
      themeMaterial = "dark"
    }
	});
</script>

<MaterialAppMin theme={themeMaterial}>
  <ProtectedRoutes>
    {#if $isLoading}
      <div class="flex justify-center">
        <Spinner />
      </div>
    {:else}
      <Toaster />
      <div
        class="flex flex-col items-center justify-center min-h-screen shadow-lg background-card"
      >
        <div
          class="flex flex-col items-center justify-center p-4 shadow rounded-lg w-3/4 border space-y-3"
        >
          <h2 class="text-2xl font-bold mb-4 text-center">Account Settings</h2>

          <!-- Profile Picture -->
          <div
            class="flex flex-col items-center mb-4 rounded-full border avatar-container"
          >
            <Avatar size="15rem">
              <img
                src={user.profile_picture}
                alt="Avatar"
                class="avatar-image"
              />
              <div
                class="absolute inset-0 flex items-center justify-center cursor-pointer hover:bg-black hover:bg-opacity-50 transition-all duration-300"
                on:click={redirectToGravatar}
              >
                <Icon path={mdiLaunch} size="2rem" class="text-white" />
              </div>
            </Avatar>
            <Tooltip bottom>
              <div slot="activator">
                Change avatar on Gravatar
              </div>
            </Tooltip>
          </div>

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

          <div class="w-1/2 flex flex-col gap-5">
            <!-- Change Password -->
            <Button class="bg-highVizLight-primary text-black" rounded 
            on:click={changePassword}
            >Change Password?</Button
            >
            
            <!-- Save Changes -->
            <Button
            class="bg-highVizLight-primary text-black" rounded
            on:click={saveChanges}>Save Changes</Button
            >
          </div>
        </div>
      </div>
    {/if}
  </ProtectedRoutes>
</MaterialAppMin>

<style>
  .avatar-container {
    position: relative;
    overflow: hidden;
  }

  .avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Remove other avatar-related styles */
</style>
