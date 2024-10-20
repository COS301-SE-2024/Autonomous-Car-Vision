<script>
    import { Button, TextField, Icon, } from "svelte-materialify";
    import axios from "axios";
    import { push } from "svelte-spa-router";
    import {theme } from "../stores/themeStore";
    import { onMount } from "svelte";

    let HOST_IP;
    onMount(async () => {
      HOST_IP = await window.electronAPI.getHostIp();
    });

    let teamName = "";

    const submit = async () => {
      try{
        const response = await axios.post("http://" + HOST_IP + ":8000/createTeam/", {
          teamName: teamName,
          uid: window.electronAPI.getUid(),
          admin: true,
        });
      window.electronAPI.storeTeamName(teamName);
        push("/invite");
      } catch (error) {
        console.error("Creating a team failed:", error);
      }
    };
  
  </script>
  
  {#if $theme === 'highVizLight'}
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClassLight">
      <div class="flex flex-row ">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/join"
        >
          <Button
            class="text-black "
            depressed
            block>Join Team</Button
          >
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-dark-primary"
          href="#/newTeam"
        >
          <Button
            class="text-black "
            depressed
            block>New Team</Button
          >
        </a>
      </div>
      <div class="w-full p-4 rounded-md mt-2 text-black shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-black">Start a new!</h1>
          <p class="text-black">Please enter a new team name below.</p>
        </div>

          <div id="form" class="flex flex-col gap-2 py-3 text-white">
            <TextField bind:value={teamName} outlined class="border-b border-dark-primary ">Team name
            </TextField>

             <div> 
                <a
                class="w-full mt-4 h-8 flex flex-col flex-wrap justify-center items-center"
                href="#/invite"
                >
                <Button
                class="bg-theme-dark-primary text-theme-dark-lightText"
                rounded
                block on:click={submit}>Next</Button
                >
             </div>
          </div>
          </div>      
      </div>
    </div>
  {:else}
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClass">
      <div class="flex flex-row ">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/join"
        >
          <Button
            class="text-white "
            depressed
            block>Join Team</Button
          >
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-dark-primary"
          href="#/newTeam"
        >
          <Button
            class="text-white "
            depressed
            block>New Team</Button
          >
        </a>
      </div>
      <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-white">Start a new!</h1>
          <p class="text-white">Please enter a new team name below.</p>
        </div>

          <div id="form" class="flex flex-col gap-2 py-3 text-white">
            <TextField bind:value={teamName} outlined class="border-b border-dark-primary ">Team name
            </TextField>

             <div> 
                <a
                class="w-full mt-4 h-8 flex flex-col flex-wrap justify-center items-center"
                href="#/invite"
                >
                <Button
                class="bg-theme-dark-primary text-theme-dark-lightText"
                rounded
                block on:click={submit}>Next</Button
                >
             </div>
          </div>
          </div>
        
      </div>
    </div>
  {/if}  
  
  <style>
      .containerClass{
        background-image: linear-gradient(180deg,#181818, #001524 );
      }

      .containerClassLight{
      background-image: linear-gradient(180deg,#B6D9E8, #F8F8F8);
    }
  </style>