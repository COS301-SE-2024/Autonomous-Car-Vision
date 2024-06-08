<script>
  import { TextField, Button } from "svelte-materialify";
  import { onMount } from "svelte";
  import axios from "axios";

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
          uemail: localStorage.getItem("uemail"),
        });
        console.log("Salt and UID retrieved:", response.data);

        uid = response.data.uid;
        localStorage.setItem("uid", uid);
        sString = response.data.salt;
      } catch (error) {
        console.error("Failed to retrieve salt and UID:", error);
        return;
      }

      console.log("Old password:", oldPassword);
      console.log("New password:", newPassword);

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
        console.log("Token:", localStorage.getItem("token"));

        const response = await axios.post(
          "http://localhost:8000/changePassword/",
          {
            uid: localStorage.getItem("uid"),
            old_password: hashOld,
            new_password: hashNew,
            token: localStorage.getItem("token"),
          }
        );
        console.log("Password Changed:", response.data);
      } catch (error) {
        console.error("Password change failed:", error);
      }
    } else {
      alert("Passwords do not match");
    }
  };

  onMount(() => {
    const firstInput = document.querySelector("#oldPassword");
    if (firstInput) {
      firstInput.focus();
    }
  });
</script>

<div class="flex flex-col items-center justify-center min-h-screen">
  <div
    class="flex flex-col items-center justify-center p-8 rounded-lg shadow-lg w-96 border border-theme-keith-accentone space-y-3"
  >
    <h2 class="text-2xl font-bold mb-4 text-center text-theme-keith-accentone">
      Change Password
    </h2>

    <!-- Old Password -->
    <div class="mb-4">
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
    <div class="mb-4">
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
    <div class="mb-4">
      <label for="confirmPassword" class="block text-theme-keith-accentone mb-1"
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

    <!-- Change Password Button -->
    <Button class="bg-theme-keith-accentone rounded" on:click={changePassword}
      >Change Password</Button
    >
  </div>
</div>
