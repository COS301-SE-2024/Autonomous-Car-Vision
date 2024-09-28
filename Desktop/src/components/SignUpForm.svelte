<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import {theme } from "../stores/themeStore";

  function handleEnterdown(e) {
    if (e.key == "Enter") {
      onSubmit();
    }
  }

  let nToken = "";
  let eToken = "";
  let pToken = "";
  let ppToken = "";

  onMount(async () => {
    const HOST_IP = await window.electronAPI.getHostIp();
  });

  const onSubmit = async () => {
    console.log("Sign-up");
    console.log(eToken);
    console.log(pToken);
    if (pToken !== ppToken) {
      alert("Passwords do not match");
      return;
    }
    if(pToken.length == 0){
      alert("Password cannot be empty");
      return;
    }
    
    //! NEED TO MOVE SOON
    try {
      const { hash, salt } = await window.electronAPI.hashPassword(pToken);
      const response = await axios.post("http://" + HOST_IP + ":8000/signup/", {
        uname: nToken,
        uemail: eToken,
        password: hash,
        salt: salt,
        cname: "dev",
        is_admin: false,
      });
      window.electronAPI.storeUid(JSON.stringify(response.data.uid));
      window.electronAPI.storeUemail(eToken);
      //! FIX to push to otp
      window.electronAPI.storePrevPath("/signup");
      push("/otp");
      // push("/join")
    } catch (error) {
      console.error("Sign-up Failed:", error);
    }
  };
  let show = false;
  let showConfirm = false;
</script>

{#if $theme === 'highVizLight'}
  <div class=" lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClassLight">
      <!-- <MaterialApp> -->
        <div class="flex flex-row ">
          <a
            class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
            href="#/login"
          >
            <Button
              class="text-black "
              depressed
              block>Log In</Button
            >
          </a>
          <a
            class="w-full h-14 flex flex-col flex-wrap justify-center items-center  border-2 border-theme-dark-primary"
            href="#/join"
          >
            <Button
              class="text-black "
              depressed
              block>Sign Up</Button
            >
          </a>
        </div>
        <div class=" w-full p-4 rounded-lg mt-2  shadow-card text-black">
          <div class="text-left">
            <h1 class="text-2xl">Welcome!</h1>
            <p>Please enter your information to sign up.</p>
          </div>
          <div
            on:keydown={handleEnterdown}
            id="form"
            class="flex flex-col gap-2 py-3 text-white"
          >
            <TextField bind:value={eToken} outlined class="pt-4 border-b-2 border-dark-primary ">Email</TextField>
            <TextField bind:value={nToken} outlined class="pt-4 border-b-2 border-dark-primary text-theme-dark-white">Username</TextField>
            <TextField 
              bind:value={pToken}
              outlined
              type={show ? "text" : "password"}
              class="pt-4 border-b-2 border-dark-primary text-theme-dark-white"
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
              class="pt-4 border-b-2 border-dark-primary text-theme-dark-white"
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
            class="mt-4 bg-theme-dark-primary text-theme-dark-white hoverClassLight"
            on:click={onSubmit}
            rounded
            block>Sign up</Button
          >
        </div>
      <!-- </MaterialApp> -->
      </div>
  </div>
  {:else}
  <div class=" lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="containerClass">
      <!-- <MaterialApp> -->
        <div class="flex flex-row ">
          <a
            class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
            href="#/login"
          >
            <Button
              class="text-white "
              depressed
              block>Log In</Button
            >
          </a>
          <a
            class="w-full h-14 flex flex-col flex-wrap justify-center items-center border-2 border-dark-primary"
            href="#/join"
          >
            <Button
              class="text-white "
              depressed
              block>Sign Up</Button
            >
          </a>
        </div>
        <div class=" w-full p-4 rounded-lg mt-2  shadow-card text-white">
          <div class="text-left">
            <h1 class="text-2xl">Welcome!</h1>
            <p>Please enter your information to sign up.</p>
          </div>
          <div
            on:keydown={handleEnterdown}
            id="form"
            class="flex flex-col gap-2 py-3 text-white"
          >
            <TextField bind:value={eToken} outlined class="pt-4 border-b-2 border-dark-primary ">Email</TextField>
            <TextField bind:value={nToken} outlined class="pt-4 border-b-2 border-dark-primary text-theme-dark-white">Username</TextField>
            <TextField 
              bind:value={pToken}
              outlined
              type={show ? "text" : "password"}
              class="pt-4 border-b-2 border-dark-primary text-theme-dark-white"
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
              class="pt-4 border-b-2 border-dark-primary text-theme-dark-white"
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
            class="mt-4 bg-theme-dark-primary text-theme-dark-white hoverClass"
            on:click={onSubmit}
            rounded
            block>Sign up</Button
          >
        </div>
      <!-- </MaterialApp> -->
      </div>
  </div>
  {/if}

<style>

  .custom-text-field input {
    color: #f56565; /* Tailwind CSS red-500 color */
  }

  .containerClass{
  background-image: linear-gradient(180deg,#181818, #001524 );
}

.containerClassLight{
  background-image: linear-gradient(180deg,#B6D9E8, #F8F8F8);
}

.fillUp{
  color: #001524;
}

.hoverClass{
    background-image: #012431b1;
}

.hoverClassLight {
    background-image: #377482c6;
  }

</style>
