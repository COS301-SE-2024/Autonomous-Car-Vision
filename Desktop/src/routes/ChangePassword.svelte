<script>
  import { TextField, Button } from "svelte-materialify";
  import { onMount } from "svelte";
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
  import toast, { Toaster } from "svelte-french-toast";

  // Loading screen imports
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let oldPassword = "";
  let newPassword = "";
  let confirmPassword = "";
  let passwordsMatch = true;

  function checkPasswordsMatch() {
    passwordsMatch = newPassword === confirmPassword;
  }

  const changePassword = async () => {
    checkPasswordsMatch();
    let sString = "";
    let uid = 0;
    if (passwordsMatch) {
      try {
        const response = await axios.post("http://localhost:8000/getSalt/", {
          uemail: window.electronAPI.getUemail(),
        });
        console.log("Salt and UID retrieved:", response.data);

        uid = response.data.uid;
        window.electronAPI.storeUid(uid);
        sString = response.data.salt;
      } catch (error) {
        console.error("Failed to retrieve salt and UID:", error);
        return;
      }

      try {
        const { hash: hashOld } = await window.electronAPI.hashPasswordSalt(
          oldPassword,
          sString
        );

        const { hash: hashNew } = await window.electronAPI.hashPasswordSalt(
          newPassword,
          sString
        );

        console.log("Hashed Passwords:", hashOld, hashNew);
        console.log("UID:", uid);
        console.log("Token:", window.electronAPI.getToken());

        const response = await axios.post(
          "http://localhost:8000/changePassword/",
          {
            uid: window.electronAPI.getUid(),
            old_password: hashOld,
            new_password: hashNew,
            token: window.electronAPI.getToken(),
          }
        );
        console.log("Password Changed:", response.data);

        if (response.data.status === "200") {
          toast.success("Password changed successfully!", {
            duration: 5000,
            position: "top-center",
          });
          push("/accountSettings");
        }
      } catch (error) {
        console.error("Password change failed:", error);
        toast.error("Failed to change password", {
          duration: 5000,
          position: "top-center",
        });
      }
    } else {
      alert("Passwords do not match");
    }
  };

  // For loading screen purposes
  onMount(() => {
    isLoading.set(true);
    const firstInput = document.querySelector("#oldPassword");
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
    <div class="flex flex-col items-center justify-center min-h-screen">
      <div
        class="flex flex-col items-center justify-center p-8 rounded-lg shadow-lg w-1/2 border border-theme-keith-accentone space-y-3"
      >
        <h2
          class="text-2xl font-bold mb-4 text-center text-theme-keith-accentone"
        >
          Change Password
        </h2>

        <!-- Old Password -->
        <div class="mb-4 w-1/2">
          <label for="oldPassword" class="block text-theme-keith-accentone mb-1"
            >Old Password</label
          >
          <TextField
            id="oldPassword"
            type="password"
            bind:value={oldPassword}
            class="w-full p-2 border border-green rounded"
          />
        </div>

        <!-- New Password -->
        <div class="mb-4 w-1/2">
          <label for="newPassword" class="block text-theme-keith-accentone mb-1"
            >New Password</label
          >
          <TextField
            id="newPassword"
            type="password"
            bind:value={newPassword}
            class="w-full p-2 border border--theme-keith-accentone rounded"
          />
        </div>

        <!-- Confirm New Password -->
        <div class="mb-4 w-1/2">
          <label
            for="confirmPassword"
            class="block text-theme-keith-accentone mb-1"
            >Confirm New Password</label
          >
          <TextField
            id="confirmPassword"
            type="password"
            bind:value={confirmPassword}
            on:input={checkPasswordsMatch}
            class="w-full p-2 border border--theme-keith-accentone rounded"
          />
          {#if !passwordsMatch}
            <p class="text-theme-keith-highlight mt-1">
              The passwords do not match
            </p>
          {/if}
        </div>

        <!-- return button -->
        <Button
          class="shadow-none rounded"
          on:click={() => push("/accountSettings")}>Return?</Button
        >

        <!-- Change Password Button -->
        <Button
          class="bg-theme-keith-accentone rounded"
          on:click={changePassword}>Change Password</Button
        >
      </div>
    </div>
  {/if}
</ProtectedRoutes>
