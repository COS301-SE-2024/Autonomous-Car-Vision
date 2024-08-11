<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";

  // Loading screen imports
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

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

<!-- TODO: add error messages -->
<div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
  <div class="container">
  <!-- <MaterialApp> -->
    <div class="flex flex-row ">
      <a
        class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-dark-primary "
        href="#/login"
      >
        <Button
          class="text-white "
          depressed
          block>Log In</Button
        >
      </a>
      <a
        class="w-full h-14 flex flex-col flex-wrap justify-center items-center "
        href="#/signup"
      >
        <Button
          class="text-white "
          depressed
          block>Sign Up</Button
        >
      </a>
    </div>
    <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
      <div class="text-left">
        <h1 class="text-2xl text-white">Welcome back!</h1>
        <p class="text-white">Please enter your information.</p>
      </div>
      {#if step === 1}
        <div id="form" class="flex flex-col gap-2 py-3 text-white">
          <TextField bind:value={nToken} outlined class="border border-dark-primary ">Username/Email</TextField>
          <Button
            class="bg-theme-dark-primary text-theme-dark-lightText"
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
            class="bg-theme-dark-primary text-theme-dark-lightText"
            on:click={onSubmitPassword}
            rounded
            block>Log in</Button
          >
        </div>
      {/if}
    </div>
  <!-- </MaterialApp> -->
  </div>
</div>


<style>
    .container{
      background-image: linear-gradient(180deg,#181818, #001524 );
    }
</style>