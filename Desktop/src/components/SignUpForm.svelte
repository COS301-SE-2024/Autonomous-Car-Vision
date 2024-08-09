<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";

  function handleEnterdown(e) {
    if (e.key == "Enter") {
      onSubmit();
    }
  }

  let nToken = "";
  let eToken = "";
  let pToken = "";
  let ppToken = "";

  const onSubmit = async () => {
    console.log("Sign-up");
    console.log(eToken);
    console.log(pToken);
    if (pToken !== ppToken) {
      alert("Passwords do not match");
      return;
    }
    try {
      const { hash, salt } = await window.electronAPI.hashPassword(pToken);
      const response = await axios.post("http://localhost:8000/signup/", {
        uname: nToken,
        uemail: eToken,
        password: hash,
        salt: salt,
      });
      window.electronAPI.storeUid(JSON.stringify(response.data.uid));

      push("/otp");
    } catch (error) {
      console.error("Sign-up Failed:", error);
    }
  };
  let show = false;
  let showConfirm = false;
</script>

<div class=" lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
  <div class="container">
    <MaterialApp>
      <div class="container flex flex-row gap-2 rounded-lg bg-none">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/login"
        >
          <Button
            class="text-theme-dark-white bg-theme-dark-white "
            depressed
            block>Log In</Button
          >
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border border-theme-dark-primary rounded-md"
          href="#/signup"
        >
          <Button
            class="text-black bg-theme-dark-primary"
            depressed
            block>Sign Up</Button
          >
        </a>
      </div>
      <div class="continer w-full p-4 rounded-lg mt-2  shadow-card text-black">
        <div class="text-left">
          <h1 class="text-2xl">Welcome!</h1>
          <p>Please enter your information to sign up.</p>
        </div>
        <div
          on:keydown={handleEnterdown}
          id="form"
          class="flex flex-col gap-1 py-2 text-white"
        >
          <TextField bind:value={eToken} outlined class="text-theme-dark-white">Email</TextField>
          <TextField bind:value={nToken} outlined>Username</TextField>
          <TextField
            bind:value={pToken}
            outlined
            type={show ? "text" : "password"}
          >
            Password
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
              slot="append"
              on:click={() => {
                show = !show;
              }}
            >
              <Icon path={show ? mdiEyeOff : mdiEye} class="text-theme-dark-primary"/>
            </div>
          </TextField>
          <TextField
            bind:value={ppToken}
            outlined
            type={showConfirm ? "text" : "password"}
          >
            Confirm password
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
              slot="append"
              on:click={() => {
                showConfirm = !showConfirm;
              }}
            >
              <Icon path={showConfirm ? mdiEyeOff : mdiEye} class="text-theme-dark-primary"/>
            </div>
          </TextField>
        </div>
        <Button
          class="bg-theme-dark-primary text-theme-dark-white"
          on:click={onSubmit}
          rounded
          block>Sign up</Button
        >
      </div>
    </MaterialApp>
    </div>
</div>

<style>

  .custom-text-field input {
    color: #f56565; /* Tailwind CSS red-500 color */
  }

  .container{
  background-image: linear-gradient(180deg, #001524, #181818);
}
</style>
