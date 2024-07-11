<script>
  import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
  import { mdiEyeOff, mdiEye } from "@mdi/js";
  import axios from "axios";
  import { push } from "svelte-spa-router";

  function handleEnterdown(e) {
    if (e.key == "Enter") {
      onSubmit();
    }
  }

  let nToken = "";
  let eToken = "";
  let pToken = "";
  let ppToken = "";

  const onSubmit = async () => {
    console.log("Sign-up");
    console.log(eToken);
    console.log(pToken);
    if (pToken !== ppToken) {
      alert("Passwords do not match");
      return;
    }
    try {
      const { hash, salt } = await window.electronAPI.hashPassword(pToken);
      const response = await axios.post("http://localhost:8000/signup/", {
        uname: nToken,
        uemail: eToken,
        password: hash,
        salt: salt,
      });
      window.electronAPI.storeUid(JSON.stringify(response.data.uid));

      push("/otp");
    } catch (error) {
      console.error("Sign-up Failed:", error);
    }
  };
  let show = false;
  let showConfirm = false;
</script>

<MaterialApp>
    <div class="glass">
      <div class="flex flex-row gap-2">
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
          href="#/login"
        >
          <Button
            class="text-theme-dark-white bg-theme-dark-primary "
            depressed
            block>Log In</Button
          >
        </a>
        <a
          class="w-full h-14 flex flex-col flex-wrap justify-center items-center border border-theme-dark-primary rounded-md"
          href="#/signup"
        >
          <Button class="text-black" depressed block>Sign Up</Button>
        </a>
      </div>
      <div class="w-full p-4 rounded-md mt-2 text-black">
        <div class="text-left">
          <h1 class="text-2xl">Welcome!</h1>
          <p>Please enter your information to sign up.</p>
        </div>
        <div
          on:keydown={handleEnterdown}
          id="form"
          class="flex flex-col gap-1 py-2"
        >
          <TextField bind:value={eToken} outlined class="text-theme-dark-white"
            >Email</TextField
          >
          <TextField bind:value={nToken} outlined>Username</TextField>
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
              <Icon
                path={show ? mdiEyeOff : mdiEye}
                class="text-theme-dark-primary"
              />
            </div>
          </TextField>
          <TextField
            bind:value={ppToken}
            outlined
            type={showConfirm ? "text" : "password"}
          >
            Confirm password
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
              slot="append"
              on:click={() => {
                showConfirm = !showConfirm;
              }}
            >
              <Icon
                path={showConfirm ? mdiEyeOff : mdiEye}
                class="text-theme-dark-primary"
              />
            </div>
          </TextField>
        </div>
        <Button
          class="bg-theme-dark-primary text-theme-dark-white"
          on:click={onSubmit}
          rounded
          block>Sign up</Button
        >
      </div>
    </div>
</MaterialApp>

<style>
  .custom-text-field input {
    color: #f56565; /* Tailwind CSS red-500 color */
  }

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
