<script>
    import { Button, TextField, Icon, } from "svelte-materialify";
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
      <div class="w-full p-4 rounded-md mt-2 text-white shadow-card">
        <div class="text-left">
          <h1 class="text-2xl text-white">Join a team!</h1>
          <p class="text-white">Please enter the team name below.</p>
        </div>
        {#if step === 1}
          <div id="form" class="flex flex-col gap-2 py-3 text-white">
            <TextField outlined class="border border-dark-primary ">Username/Email</TextField>
            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText"
              on:click={onSubmitUsername}
              rounded
              block>Next</Button
            >
          </div>
        {/if}
          </div>
        
      </div>
    <!-- </MaterialApp> -->
    </div>
  
  
  <style>
      .container{
        background-image: linear-gradient(180deg,#181818, #001524 );
      }
  </style>