<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";

  let nToken = "";
  let pToken = "";
  let step = 1;
  let sString = "";
  let show = false;
  let uid = 0;

  const onSubmitUsername = async () => {
    window.electronAPI.storeUemail(nToken);
    try {
      const response = await axios.post("http://localhost:8000/getSalt/", {
        uemail: nToken,
      });
      uid = response.data.uid;
      sString = response.data.salt;
      console.log(sString);
      console.log("uid from resp:", uid);
      step = 2;
    } catch (error) {
      console.error("Failed to retrieve salt and UID:", error);
    }
  };

  const onSubmitPassword = async () => {
    console.log("Password Step");
    console.log(pToken);

    try {
      const { hash } = await window.electronAPI.hashPasswordSalt(
        pToken,
        sString
      );

      const response = await axios.post("http://localhost:8000/signin/", {
        uid: uid,
        password: hash,
      });
      window.electronAPI.storeUid(uid);
      push("/otp");
    } catch (error) {
      console.error("Login Failed:", error);
    }
  };
</script>

<div class="min-h-screen lg:w-4/12 w-6/12 mx-auto py-4 my-4 bg-theme-dark-background">
  <MaterialApp class="bg-theme-dark-background">
    <div class="flex flex-row gap-2 bg-theme-dark-background">
      <a
        class="w-full h-14 flex flex-col flex-wrap justify-center items-center bg-theme-dark-background"
        href="#/login"
      >
        <Button
          class="text-theme-dark-lightText bg-theme-dark-secondary hover:bg-theme-dark-secondary transition-colors"
          depressed
          block>Log In</Button
        >
      </a>
      <a
        class="w-full h-14 flex flex-col flex-wrap justify-center items-center bg-theme-dark-background"
        href="#/signup"
      >
        <Button
          class="text-theme-dark-lightText bg-theme-dark-primary hover:bg-theme-dark-secondary transition-colors"
          depressed
          block>Sign Up</Button
        >
      </a>
    </div>
    <div class="w-full p-4 border-2 rounded-md border-theme-dark-secondary mt-2 bg-theme-dark-background shadow-tech-blue">
      <div class="text-left text-theme-dark-primary">
        <h1 class="text-2xl">Welcome back!</h1>
        <p class="text-theme-dark-secondary">Please enter your information.</p>
      </div>
      {#if step === 1}
        <div id="form" class="flex flex-col gap-1 py-2">
          <TextField bind:value={nToken} outlined class="outline-theme-dark-primary">Username/Email</TextField>
          <Button
            class="bg-theme-dark-secondary text-theme-dark-lightText"
            on:click={onSubmitUsername}
            rounded
            block>Next</Button
          >
        </div>
      {/if}
      {#if step === 2}
        <div id="form" class="flex flex-col gap-1 py-2">
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
              <Icon path={show ? mdiEyeOff : mdiEye} />
            </div>
          </TextField>
          <Button
            class="bg-theme-keith-accentone text-theme-keith-jet"
            on:click={onSubmitPassword}
            rounded
            block>Log in</Button
          >
        </div>
      {/if}
    </div>
  </MaterialApp>
</div>
