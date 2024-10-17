<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import {theme} from '../stores/themeStore';
  import { onMount } from "svelte";
  // Loading screen imports
  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let nToken = "";
  let pToken = "";
  let step = 1;
  let sString = "";
  let show = false;
  let uid = 0;
  let HOST_IP;
  onMount(async () => {
     HOST_IP = await window.electronAPI.getHostIp();
  });

  const onSubmitUsername = async () => {
    window.electronAPI.storeUemail(nToken);
    try {
      const response = await axios.post("http://" + HOST_IP + ":8000/getSalt/", {
        uemail: nToken,
      });
      uid = response.data.uid;
      sString = response.data.salt;
      step = 2;
    } catch (error) {
      console.error("Failed to retrieve salt and UID:", error);
    }
  };

  const onSubmitPassword = async () => {

    try {
      const { hash } = await window.electronAPI.hashPasswordSalt(
        pToken,
        sString
      );

      const response = await axios.post("http://" + HOST_IP + ":8000/signin/", {
        uid: uid,
        password: hash,
      });
      window.electronAPI.storeUid(uid);
      window.electronAPI.storePrevPath("/login");
      push("/otp");
    } catch (error) {
      console.error("Login Failed:", error);
    }
  };
</script>

<!-- TODO: add error messages -->
{#if $theme === 'highVizLight'}
<div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
  <div class="containerClassLight">
  <!-- <MaterialApp> -->
    <div class="flex flex-row ">
      <a
        class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-theme-dark-primary "
        href="#/login"
      >
        <Button
          class="text-black "
          depressed
          block>Log In</Button
        >
      </a>
      <a
        class="w-full h-14 flex flex-col flex-wrap justify-center items-center "
        href="#/signup"
      >
        <Button
          class="text-black "
          depressed
          block>Sign Up</Button
        >
      </a>
    </div>
    <div class="w-full p-4 rounded-md mt-2 text-black shadow-card">
      <div class="text-left">
        <h1 class="text-2xl text-black">Welcome back!</h1>
        <p class="text-black">Please enter your information.</p>
      </div>
      {#if step === 1}
        <div id="form" class="flex flex-col gap-2 py-3 text-white">
          <TextField bind:value={nToken} outlined class="pt-4 border-b-2 border-dark-primary ">Username/Email</TextField>
          <div class="flex mt-4 gap-2">
            <a href="#/" class="w-full">
              <Button
                rounded
                class=" py-2 bg-theme-dark-primary text-white hoverClassLight transition"
              >
                ↤ Back
             </Button>
            </a>
            <Button
              class=" bg-theme-dark-primary text-theme-dark-lightText"
              on:click={onSubmitUsername}
              rounded
              >Next  ↦</Button
            >
          </div>
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
            class="mt-4 bg-theme-dark-primary text-theme-dark-lightText"
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
{:else}
<div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
  <div class="containerClass">
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
          <TextField bind:value={nToken} outlined class="pt-4 border-b-2 border-dark-primary ">Username/Email</TextField>
          <Button
            class="mt-4 bg-theme-dark-primary text-theme-dark-lightText"
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
          <div class="flex mt-4 gap-2">
            <a href="#/" class="w-full">
              <Button
                rounded
                class=" py-2 bg-theme-dark-primary text-white hoverClassLight transition"
              >
                ↤ Back
             </Button>
            </a>
            <Button
              class=" bg-theme-dark-primary text-theme-dark-lightText"
              on:click={onSubmitUsername}
              rounded
              >Next  ↦</Button
            >
          </div>
        </div>
      {/if}
    </div>
  <!-- </MaterialApp> -->
  </div>
</div>

{/if}



<style>
    .containerClass{
      background-image: linear-gradient(180deg,#181818, #001524 );
    }

    .containerClassLight {
     background-image: linear-gradient(180deg,#B6D9E8, #F8F8F8 );
}
</style>