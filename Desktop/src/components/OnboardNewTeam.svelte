<script>
    import { Button, TextField, Icon, } from "svelte-materialify";
    import axios from "axios";
    import { push } from "svelte-spa-router";

    let teamName = "";

    const submit = async () => {
      console.log("Creating a new team");

      // check if team exists, if not, create team and add user to team
      try{
        const response = await axios.post("http://localhost:8000/createTeam/", {
          teamName: teamName,
          uid: window.electronAPI.getUid(),
          admin: true,
        });
      window.electronAPI.storeTeamName(teamName);
        console.log(response);
        push("/invite");
      } catch (error) {
        console.error("Creating a team failed:", error);
      }
    };
  
  </script>
  
  <!-- TODO: add error messages -->
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="container">
    <!-- <MaterialApp> -->
      <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-white">Start a new!</h1>
          <p class="text-white">Please enter a new team name below.</p>
        </div>
       <!-- TODO: check for uniqueness: if not, make box red and button grey. else, fine -->

          <div id="form" class="flex flex-col gap-2 py-3 text-white">
            <TextField bind:value={teamName} outlined class="border border-dark-primary ">Team name
            </TextField>

            <!-- TODO: link next button to next page -->
             <div> 
                <a
                class="w-full h-8 flex flex-col flex-wrap justify-center items-center"
                href="#/"
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
    <!-- </MaterialApp> -->
    </div>
  
  
  <style>
      .container{
        background-image: linear-gradient(180deg,#181818, #001524 );
      }
  </style>