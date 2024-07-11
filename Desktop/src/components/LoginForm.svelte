<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
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
        sString,
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
<MaterialApp>
    <div class="glass">
      <div class="flex flex-row gap-2">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border border-theme-dark-primary rounded-md"
          href="#/login"
        >
          <Button class="text-black " depressed block>Log In</Button>
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/signup"
        >
          <Button
            class="text-theme-dark-white bg-theme-dark-primary"
            depressed
            block>Sign Up</Button
          >
        </a>
      </div>
      <div class="w-full p-4 rounded-md mt-2">
        <div class="text-left">
          <h1 class="text-2xl text-black">Welcome back!</h1>
          <p class="text-black">Please enter your information.</p>
        </div>
        {#if step === 1}
          <div id="form" class="flex flex-col gap-1 py-2">
            <TextField bind:value={nToken} outlined>Username/Email</TextField>
            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText"
              on:click={onSubmitUsername}
              rounded
              block>Next</Button
            >
          </div>
        {/if}
        {#if step === 2}
          <div id="form" class="flex flex-col gap-1 py-2">
            <TextField
              bind:value={pToken}
              outlined
              type={show ? "text" : "password"}
            >
              Password
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <div
                slot="append"
                on:click={() => {
                  show = !show;
                }}
              >
                <Icon path={show ? mdiEyeOff : mdiEye} />
              </div>
            </TextField>
            <Button
              class="bg-theme-dark-primary text-theme-dark-lightText"
              on:click={onSubmitPassword}
              rounded
              block>Log in</Button
            >
          </div>
        {/if}
      </div>
    </div>
</MaterialApp>

<style>
  .glass {
    position: relative;
    top: 200px;
    z-index: 10;
    background: rgba(255, 255, 255, 0.25098039215686274);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.2px);
    padding: 2rem;
    width: 100%;
  }
</style>
