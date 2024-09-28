<script>
    import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
    import { mdiAccountPlus } from "@mdi/js";
  import { push } from "svelte-spa-router";
  import axios from "axios";

    let add;
    let email = ''; // Variable to store the email address
    let newMembers = []; // Array to store the list of new members

    onMount(async () => {
        const HOST_IP = await window.electronAPI.getHostIp();
    });

    function addMember() {
        if (email.trim()) {
        newMembers = [...newMembers, email.trim()]; // Add the email to the array
        email = ''; // Clear the email field
        }
    }

    const goToTutorial = async () => {
        push("/install");
    }

    const sendEmails = async () => {
        console.log("Sending invites");
        console.log(newMembers);
        // Send the emails to the new members
        try {
            const response = await axios.post("http://" + HOST_IP + ":8000/sendInviteEmail/", {
                newMembers: newMembers,
                teamName: window.electronAPI.getTeamName(),
            });
            console.log(response);
            push("/install");
        } catch (error) {
            console.error("Sending invites failed:", error);
        }
    };
  
  </script>

<div class=" lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClass">
      <!-- <MaterialApp> -->
        <div class=" w-full p-4 rounded-lg mt-2  shadow-card text-white">
          <div class="text-left">
            <h1 class="text-2xl">Invite!</h1>
            <p>Please enter the emails of your new team members below.</p>
          </div>
          <div id="form" class="flex flex-col gap-2 py-3 text-white">
            <TextField 
                bind:value={email}
                outlined 
                class="border-b border-dark-primary ">Email address

                 <!-- svelte-ignore a11y-click-events-have-key-events -->
                 <div
                 slot="append"
                 on:click={addMember}
               >
                 <Icon path={mdiAccountPlus} class="text-theme-dark-primary cursor-pointer"/>
               </div>
            </TextField>
          </div>

          <div class="flex gap-2 newMember content-fit">
            {#each newMembers as member}
                <p class="bg-theme-dark-primary rounded-lg px-1 mt-2 text-theme-dark-white hoverClass">{member}</p>
             {/each}
    

          </div>
        </div>
            <!-- TODO: Link the send invites button to next page -->
                <div> 
                    <a  
                        class="w-full h-8 flex flex-col flex-wrap justify-center items-center"
                        href="#/installGuide"
                        >
                        <Button
                            class="bg-theme-dark-primary mt-4 w-2/3 text-theme-dark-white"
                            rounded
                            block on:click={sendEmails}>Send Invites</Button
                        > 
                    </a>
                </div>
          <!-- TODO: Link the skip button to next page -->
          <div  class="ml-96 pl-6 text-theme-dark-white pt-2 rounded">
                <Button on:click={goToTutorial} class="rounded">Skip Step</Button>
            </div>
        </div>
      <!-- </MaterialApp> -->
    </div>
  
  <style>
  
    .containerClass{
    background-image: linear-gradient(180deg,#181818, #001524 );
  }
  </style>
  