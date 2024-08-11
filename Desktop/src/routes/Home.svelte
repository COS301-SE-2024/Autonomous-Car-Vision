<script>
  import { onMount } from "svelte";
  import { Button, MaterialApp } from "svelte-materialify";
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import { token } from "../stores/auth";

  onMount(() => {
    window.electronAPI.clearToken();
    window.electronAPI.clearUid();
    window.electronAPI.clearUname();
    window.electronAPI.clearUemail();
  });

  const developerLogin = async () => {
    try {
      const response = await axios.get("http://localhost:8000/devLogin/", {});
      console.log("Developer Login Response:", response.data);
      window.electronAPI.storeToken(response.data.token);
      window.electronAPI.storeUid(response.data.uid);
      window.electronAPI.storeUname(response.data.uname);
      window.electronAPI.storeUemail(response.data.uemail);

      console.log("Token:", window.electronAPI.getToken());
      console.log("UID:", window.electronAPI.getUid());
      console.log("UName:", window.electronAPI.getUname());
      console.log("UEmail:", window.electronAPI.getUemail());
    } catch (error) {
      console.error("Failed to login as developer:", error);
      return;
    }
    push("/gallery");
  };
</script>

<MaterialApp> 
  
  <div class="homeContainer min-h-screen flex flex-col items-center justify-center bg-theme-dark">
    
    <div> <!-- svelte-ignore a11y-missing-attribute -->
      <!-- <iframe src="https://lottie.host/embed/71d3ecd3-328d-45cc-baee-6dccec502427/2BLp8rGr90.json" class="p-1 h-64 w-96" depressed>
      </iframe> -->
      <img src="./images/HomeAnimation.gif"/>
    </div>
 
    <div
      class="modal p-8 rounded-lg shadow-lg w-80 text-theme-dark-primary"
    >
         
      <h1 class=" text-4xl text-center mb-6 text-bold text-white">Welcome to High-Viz</h1>
      <div class="flex flex-col gap-4 items-center">
        <a href="#/login" class="w-full">
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg  transition"
          >
            Log In
          </button>
        </a>
        <a href="#/signup" class="w-full">
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg  transition"
          >
            Sign Up
          </button>
        </a>
        <a href="#/" class="w-full" on:click={developerLogin}>
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg  transition"
          >
            Developer
          </button>
        </a>

        <a href="#/install" class="w-full">
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg  transition"
          >
            WIP
          </button>
        </a>
      </div>
    </div>
  </div>
</MaterialApp>


<style>
.homeContainer{
  background-image: linear-gradient(180deg, #001524, #181818);
}

.modal{
  background-image: linear-gradient(180deg, #181818, #001524);
}
button:hover {
    background-color: #0f6173c6;
  }
</style>