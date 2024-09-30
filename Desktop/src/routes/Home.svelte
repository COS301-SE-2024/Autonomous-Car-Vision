<script>
  import { onMount } from "svelte";
  import { TextField, MaterialAppMin } from "svelte-materialify";
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import { token } from "../stores/auth";
  import { theme } from "../stores/themeStore";

  let authCode = "";
  let showCodeInput = false;
  let themeMaterial = "";

  let HOST_IP;

  onMount(async () => {
    HOST_IP = await window.electronAPI.getHostIp();
    console.log("HOST_IP:", HOST_IP);
    window.electronAPI.clearToken();
    window.electronAPI.clearUid();
    window.electronAPI.clearUname();
    window.electronAPI.clearUemail();
    window.electronAPI.clearPrevPath();
    window.electronAPI.clearTeamName();

    window.electronAPI.onAuthSuccess((event, result) => {
      handleAuthSuccess(result);
    });

    window.electronAPI.onAuthError((event, error) => {
      console.error("Authentication error:", error);
    });
  });

  const googleLogin = async () => {
    try {
      const authUrl = await window.electronAPI.getAuthUrl();
      window.open(authUrl, "_blank");
      showCodeInput = true;
    } catch (error) {
      console.error("Error getting auth URL:", error);
    }
  };

  const googleLoginTest = async () => {
    try {
      const authUrl = await window.electronAPI.getAuthUrlTest();
      console.log("Auth URL:", authUrl);
      window.electronAPI.openExternal(authUrl);
    } catch (error) {
      console.error("Error getting auth URL:", error);
    }
  };

  const handleAuthSuccess = async (result) => {
    console.log("Google Sign-In Result:", result);
    window.electronAPI.storeToken(result.tokens.access_token.substring(0, 40));
    window.electronAPI.storeUid(result.user.id.substring(0, 10));
    window.electronAPI.storeUname(result.user.name);
    window.electronAPI.storeUemail(result.user.email);

    // check if user is already in the database
    const userExists = await axios.post(
      "http://" + HOST_IP + ":8000/userExists/",
      {
        email: result.user.email,
      },
    );
    if (userExists.data.exists) {
      console.log("User already exists in database");
      console.log("Token:", window.electronAPI.getToken());
      const storeTokenNow = await axios.post(
        "http://" + HOST_IP + ":8000/storeToken/",
        {
          uid: window.electronAPI.getUid(),
          token: window.electronAPI.getToken(),
        },
      );

      window.electronAPI.storeTeamName(userExists.data.teamName);
      push("/gallery");
    } else {
      console.log("User does not exist in database");
      window.electronAPI.storeTeamName("dev");

      const createUser = await axios.post(
        "http://" + HOST_IP + ":8000/signup/",
        {
          uname: result.user.name,
          uemail: result.user.email,
          password: "",
          salt: "",
          cname: "dev",
          is_admin: false,
          uid: window.electronAPI.getUid(),
        },
      );
      console.log("User created:", createUser);

      const storeTokenNow = await axios.post(
        "http://" + HOST_IP + ":8000/storeToken/",
        {
          uid: window.electronAPI.getUid(),
          token: window.electronAPI.getToken(),
        },
      );

      push("/Join");
    }
  };

  const submitAuthCode = async () => {
    try {
      const result = await window.electronAPI.exchangeCode(authCode);
      if (result.success) {
        console.log("Google Sign-In Result:", result);
        window.electronAPI.storeToken(
          result.tokens.access_token.substring(0, 40),
        );
        window.electronAPI.storeUid(result.user.id.substring(0, 10));
        window.electronAPI.storeUname(result.user.name);
        window.electronAPI.storeUemail(result.user.email);

        // check if user is already in the database
        const userExists = await axios.post(
          "http://" + HOST_IP + ":8000/userExists/",
          {
            email: result.user.email,
          },
        );
        if (userExists.data.exists) {
          console.log("User already exists in database");
          console.log("Token:", window.electronAPI.getToken());
          const storeTokenNow = await axios.post(
            "http://" + HOST_IP + ":8000/storeToken/",
            {
              uid: window.electronAPI.getUid(),
              token: window.electronAPI.getToken(),
            },
          );

          window.electronAPI.storeTeamName(userExists.data.teamName);
          push("/gallery");
        } else {
          console.log("User does not exist in database");
          window.electronAPI.storeTeamName("dev");

          const createUser = await axios.post(
            "http://" + HOST_IP + ":8000/signup/",
            {
              uname: result.user.name,
              uemail: result.user.email,
              password: "",
              salt: "",
              cname: "dev",
              is_admin: false,
              uid: window.electronAPI.getUid(),
            },
          );
          console.log("User created:", createUser);

          const storeTokenNow = await axios.post(
            "http://" + HOST_IP + ":8000/storeToken/",
            {
              uid: window.electronAPI.getUid(),
              token: window.electronAPI.getToken(),
            },
          );

          push("/Join");
        }
      } else {
        console.error("Failed to exchange code:", result.error);
      }
    } catch (error) {
      console.error("Error exchanging code:", error);
    }
  };

  const developerLogin = async () => {
    try {
      let url = "http://" + HOST_IP + ":8000/devLogin/";
      const response = await axios.get(url, {});
      console.log("Developer Login Response:", response.data);
      window.electronAPI.storeToken(response.data.token);
      window.electronAPI.storeUid(response.data.uid);
      window.electronAPI.storeUname(response.data.uname);
      window.electronAPI.storeUemail(response.data.uemail);
      window.electronAPI.storeTeamName("dev");

      console.log("Token:", window.electronAPI.getToken());
      console.log("UID:", window.electronAPI.getUid());
      console.log("UName:", window.electronAPI.getUname());
      console.log("UEmail:", window.electronAPI.getUemail());
      console.log("TeamName:", window.electronAPI.getTeamName());
    } catch (error) {
      console.error("Failed to login as developer:", error);
      return;
    }
    push("/gallery");
  };

  theme.subscribe((value) => {
    if (value == "highVizLight") {
      themeMaterial = "light";
    } else {
      themeMaterial = "dark";
    }
  });
</script>

<MaterialAppMin theme={themeMaterial}>
  {#if $theme === "highVizLight"}
    <div
      class="homeContainerLight min-h-screen flex flex-col items-center justify-center bg-theme-highVizLight"
    >
      <div class="modalLight p-8 rounded-lg shadow-lg w-1/2">
        <h1 class="text-4xl text-center mb-6 font-bold text-black">
          Welcome to High-Viz
        </h1>
        <div class="flex flex-col gap-4 items-center">
          <a href="#/login" class="w-full">
            <button
              class="w-full py-2 bg-theme-highVizLight-primary text-white rounded-lg transition"
            >
              Log In
            </button>
          </a>
          <a href="#/signup" class="w-full">
            <button
              class="w-full py-2 bg-theme-highVizLight-primary text-white rounded-lg transition"
            >
              Sign Up
            </button>
          </a>
          {#if !showCodeInput}
            <a href="#/" class="w-full" on:click={googleLogin}>
              <button
                class="w-full py-2 bg-theme-highVizLight-primary text-white rounded-lg transition"
              >
                Log In with Google
              </button>
            </a>
          {:else}
            <TextField
              bind:value={authCode}
              dense
              outlined
              class="text-dark-primary w-full"
              >Enter Authorization Code</TextField
            >
            <div class="flex flex-row gap-2 w-full">
              <button
                on:click={submitAuthCode}
                class="w-full py-2 bg-theme-highVizLight-primary text-white rounded-lg transition"
              >
                Submit Authorization Code
              </button>
              <a href="#/" class="w-full" on:click={googleLogin}>
                <button
                  class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
                >
                  Log In with Google
                </button>
              </a>
            </div>
          {/if}
          <a href="#/" class="w-full" on:click={developerLogin}>
            <button
              class="w-full py-2 bg-theme-highVizLight-primary text-white rounded-lg transition"
            >
              Developer
            </button>
          </a>
        </div>
      </div>
    </div>
  {:else}
    <div
      class="homeContainer min-h-screen flex flex-col items-center justify-center bg-theme-highVizDark"
    >
      <div class="modal p-8 rounded-lg shadow-lg w-1/2">
        <h1 class="text-4xl text-center mb-6 font-bold text-white">
          Welcome to High-Viz
        </h1>
        <div class="flex flex-col gap-4 items-center">
          <a href="#/login" class="w-full">
            <button
              class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
            >
              Log In
            </button>
          </a>
          <a href="#/signup" class="w-full">
            <button
              class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
            >
              Sign Up
            </button>
          </a>
          {#if !showCodeInput}
            <a href="#/" class="w-full" on:click={googleLogin}>
              <button
                class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
              >
                Log In with Google
              </button>
            </a>
          {:else}
            <TextField
              bind:value={authCode}
              dense
              outlined
              class="text-dark-primary w-full"
              >Enter Authorization Code</TextField
            >
            <div class="flex flex-row gap-2 w-full">
              <button
                on:click={submitAuthCode}
                class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
              >
                Submit Authorization Code
              </button>
              <a href="#/" class="w-full" on:click={googleLogin}>
                <button
                  class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
                >
                  Log In with Google
                </button>
              </a>
            </div>
          {/if}
          <a href="#/" class="w-full" on:click={developerLogin}>
            <button
              class="w-full py-2 bg-theme-dark-primary text-white rounded-lg transition"
            >
              Developer
            </button>
          </a>
        </div>
      </div>
    </div>
  {/if}
</MaterialAppMin>

<style>
  .homeContainer {
    background-image: linear-gradient(180deg, #001524, #181818);
  }

  .homeContainerLight {
    background-image: linear-gradient(180deg, #b6d9e8, #f8f8f8);
  }

  .modalLight {
    background-image: linear-gradient(180deg, #f8f8f8, #b6d9e8);
  }

  .modalLight button {
    background-color: #2a5a64c6;
  }
  .modalLight button:hover {
    background-color: #377482c6;
  }

  .modal {
    background-image: linear-gradient(180deg, #181818, #001524);
  }
  button:hover {
    background-color: #0f6173c6;
  }
</style>
