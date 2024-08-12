<script>
    import { Button, TextField, Icon, } from "svelte-materialify";
    import { mdiEyeOff, mdiEye } from "@mdi/js";
    import axios from "axios";
    import { push } from "svelte-spa-router";
  import { token } from "../stores/auth";

    let teamName = "";
    let tokenValue = "";
  
    const submit = async () => {
      console.log("Joining a team");

      // check if team exists, if not, create team and add user to team
      try{
        const response = await axios.post("http://localhost:8000/joinTeam/", {
          teamName: teamName,
          uid: window.electronAPI.getUid(),
          admin: false,
          token: tokenValue,
          email: window.electronAPI.getUemail(),
        });
        console.log(response);
        push("/install");
      } catch (error) {
        console.error("Joining a team failed:", error);
      }
    };
   
  </script>
  
  <!-- TODO: add error messages -->
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClass">
    <!-- <MaterialApp> -->
      <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-white">Join a team!</h1>
          <p class="text-white">Please enter the team name below.</p>
        </div>
          <div id="form" class="flex flex-col gap-2 py-3 text-white">
                        <!-- TODO: check if exists: if not, give sad feedback and button grey. else, fine -->

            <TextField bind:value={teamName} outlined class="border-b border-dark-primary ">Team Name</TextField>
            <TextField bind:value={tokenValue} outlined class="border-b border-dark-primary ">Token</TextField>
            <!-- TODO: Link the next button to next page -->
            <a
            class="w-full h-8 flex flex-col flex-wrap justify-center items-center"
            href="#/"
            >
            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText mt-4"
              rounded
              block on:click={submit}>Next</Button
            >
            </div>
          </div>
            <div class="m-2"> 
                <a  
                    class="w-full h-8 flex flex-col flex-wrap justify-center items-center"
                    href="#/newTeam"
                >
                    <!-- TODO: Link the button to next page -->
                    <div  class="flex flex-row ml-48 pl-4 text-theme-dark-white pt-2 rounded">

                        <p class="pt-1.5 pr-1"> Don't have a team?</p>
                        <span><Button class="rounded">Create Team</Button></span>
                    </div> 
                </a>
            </div>
          </div>
        
      </div>
    <!-- </MaterialApp> -->
    <!-- </div> -->
  
  
  <style>
      .containerClass{
        background-image: linear-gradient(180deg,#181818, #001524 );
      }
  </style>