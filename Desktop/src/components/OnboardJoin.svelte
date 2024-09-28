<script>
  import { Button, TextField, Icon } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import { token } from "../stores/auth";
  import { theme } from "../stores/themeStore";
  import { onMount } from "svelte";

  let HOST_IP;
  onMount(async () => {
    HOST_IP = await window.electronAPI.getHostIp();
  });

  let teamName = "";
  let tokenValue = "";

  const submit = async () => {
    console.log("Joining a team");

    // check if team exists, if not, create team and add user to team
    try {
      const response = await axios.post(
        "http://" + HOST_IP + ":8000/joinTeam/",
        {
          teamName: teamName,
          uid: window.electronAPI.getUid(),
          admin: false,
          token: tokenValue,
          email: window.electronAPI.getUemail(),
        },
      );
      console.log(response);
      push("/install");
    } catch (error) {
      console.error("Joining a team failed:", error);
    }
  };
</script>

{#if $theme === "highVizLight"}
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClassLight">
      <!-- <MaterialApp> -->
      <div class="flex flex-row">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-theme-dark-primary"
          href="#/join"
        >
          <Button class="text-black " depressed block>Join Team</Button>
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/newTeam"
        >
          <Button class="text-black " depressed block>New Team</Button>
        </a>
      </div>
      <div class="w-full p-4 rounded-md mt-2 text-black shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-black">Join a team!</h1>
          <p class="text-black">Please enter the team name below.</p>
        </div>
        <div id="form" class="flex flex-col gap-2 py-3 text-white">
          <!-- TODO: check if exists: if not, give sad feedback and button grey. else, fine -->

          <TextField
            bind:value={teamName}
            outlined
            class="border-b border-dark-primary ">Team Name</TextField
          >
          <TextField
            bind:value={tokenValue}
            outlined
            class="border-b border-dark-primary ">Token</TextField
          >
          <!-- TODO: Link the next button to next page -->
          <a
            class="w-full h-8 flex flex-col flex-wrap justify-center items-center"
            href="#/"
          >
            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText mt-4"
              rounded
              block
              on:click={submit}>Next</Button
            >
          </a>
        </div>
      </div>
    </div>
  </div>
{:else}
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClass">
      <!-- <MaterialApp> -->
      <div class="flex flex-row">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-dark-primary"
          href="#/join"
        >
          <Button class="text-white " depressed block>Join Team</Button>
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/newTeam"
        >
          <Button class="text-white " depressed block>New Team</Button>
        </a>
      </div>
      <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-white">Join a team!</h1>
          <p class="text-white">Please enter the team name below.</p>
        </div>
        <div id="form" class="flex flex-col gap-2 py-3 text-white">
          <!-- TODO: check if exists: if not, give sad feedback and button grey. else, fine -->

          <TextField
            bind:value={teamName}
            outlined
            class="border-b border-dark-primary ">Team Name</TextField
          >
          <TextField
            bind:value={tokenValue}
            outlined
            class="border-b border-dark-primary ">Token</TextField
          >
          <a
            class="w-full h-8 flex flex-col flex-wrap justify-center items-center"
            href="#/"
          >
            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText mt-4"
              rounded
              block
              on:click={submit}>Next</Button
            >
          </a>
        </div>
      </div>
    </div>
  </div>
{/if}

<!-- TODO: add error messages -->

<!-- </MaterialApp> -->
<!-- </div> -->

<style>
  .containerClass {
    background-image: linear-gradient(180deg, #181818, #001524);
  }

  .containerClassLight {
    background-image: linear-gradient(180deg, #b6d9e8, #f8f8f8);
  }
</style>
