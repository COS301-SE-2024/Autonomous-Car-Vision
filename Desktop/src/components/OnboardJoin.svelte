<script>
    import { Button, TextField, Icon, } from "svelte-materialify";
    import { mdiEyeOff, mdiEye } from "@mdi/js";
    import axios from "axios";
    import { push } from "svelte-spa-router";
  
   
  </script>
  
  <!-- TODO: add error messages -->
  <div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="container">
    <!-- <MaterialApp> -->
      <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-white">Join a team!</h1>
          <p class="text-white">Please enter the team name below.</p>
        </div>
          <div id="form" class="flex flex-col gap-2 py-3 text-white">
                        <!-- TODO: check if exists: if not, give sad feedback and button grey. else, fine -->

            <TextField outlined class="border border-dark-primary ">Team Name</TextField>
                    <!-- TODO: Link the next button to next page -->

            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText"
              rounded
              block>Next</Button
            >
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