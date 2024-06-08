<script>
  import { onMount } from "svelte";
  import { Button, MaterialApp } from "svelte-materialify";
  import axios from "axios";
  import { push } from "svelte-spa-router";

  onMount(() => {
    localStorage.clear();
    console.log("Cleared Local Storage");
  });

  const developerLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/devLogin/", {
        uname: "admin",
      });
      console.log("Developer Login Response:", response.data);
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("uid", response.data.uid);
      localStorage.setItem("uname", response.data.uname);
      localStorage.setItem("uemail", response.data.uemail);
    } catch (error) {
      console.error("Failed to login as developer:", error);
      return;
    }

    console.log("Developer Login Successful");
    console.log("Token:", localStorage.getItem("token"));
    console.log("UID:", localStorage.getItem("uid"));

    if (
      localStorage.getItem("token") === null ||
      localStorage.getItem("uid") === null
    ) {
      console.error("Failed to login as developer");
      return;
    }
    push("/gallary");
  };
</script>

<MaterialApp>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div
      class="bg-white p-8 rounded-lg shadow-xl w-80 border border-theme-keith-primary"
    >
      <h1 class="text-4xl text-center mb-6 text-bold">Welcome to High-Viz</h1>
      <div class="flex flex-col gap-4 items-center">
        <a href="#/login" class="w-full">
          <button
            class="w-full py-2 bg-theme-keith-accentone text-theme-keith-jet rounded-lg hover:bg-theme-keith-accenttwo transition"
          >
            Log In
          </button>
        </a>
        <a href="#/signup" class="w-full">
          <button
            class="w-full py-2 bg-theme-keith-accentone text-theme-keith-jet rounded-lg hover:bg-theme-keith-accenttwo transition"
          >
            Sign Up
          </button>
        </a>
        <a href="#/" class="w-full" on:click={developerLogin}>
          <button
            class="w-full py-2 bg-theme-keith-accentone text-theme-keith-jet rounded-lg hover:bg-theme-keith-accenttwo transition"
          >
            Developer
          </button>
        </a>
      </div>
    </div>
  </div>
</MaterialApp>
