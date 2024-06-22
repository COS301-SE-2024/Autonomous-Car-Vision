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
      token.set(response.data.token);
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
  <div class="min-h-screen flex items-center justify-center bg-theme-dark-white">
    <div
      class="p-8 rounded-lg shadow-card-blue w-80 text-theme-dark-primary bg-theme-dark-white"
    >
      <h1 class="text-4xl text-center mb-6 text-bold text-black">Welcome to High-Viz</h1>
      <div class="flex flex-col gap-4 items-center">
        <a href="#/login" class="w-full">
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg hover:bg-theme-dark-secondary transition"
          >
            Log In
          </button>
        </a>
        <a href="#/signup" class="w-full">
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg hover:bg-theme-dark-secondary transition"
          >
            Sign Up
          </button>
        </a>
        <a href="#/" class="w-full" on:click={developerLogin}>
          <button
            class="w-full py-2 bg-theme-dark-primary text-theme-dark-lightText rounded-lg hover:bg-theme-dark-secondary transition"
          >
            Developer
          </button>
        </a>
      </div>
    </div>
  </div>
</MaterialApp>
