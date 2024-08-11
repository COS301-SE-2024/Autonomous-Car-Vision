<script>
  import axios from "axios";
  import { push } from "svelte-spa-router";
  import {Button} from "svelte-materialify"

  let email = "";
  let code = Array(6).fill("");

  const verifyCode = async () => {
    const otp = code.join("");
    try {
      const response = await axios.post("http://localhost:8000/verifyOTP/", {
        uid: window.electronAPI.getUid(),
        otp: otp,
      });
      window.electronAPI.storeToken(response.data.token);
      console.log("token: ");
      console.log(window.electronAPI.getToken());
      // Update Svelte store
      // token.set(response.data.token);
      push("/gallery");
    } catch (error) {
      console.error(error);
    }
  };

  function updateCode(index, value) {
    code[index] = value;
  }

  function handleInput(e, index) {
    const value = e.target.value;
    const key = e.key;

    if (key === "Backspace") {
      if (value === "" && index > 0) {
        const previousInput = document.querySelector(`#input-${index - 1}`);
        previousInput.focus();
      }
    } else {
      updateCode(index, value);
      if (value && index < 5) {
        const nextInput = document.querySelector(`#input-${index + 1}`);
        nextInput.focus();
      }
    }
  }
</script>

<div class="flex shadow-card items-center self-center mx-auto justify-center min-h-screen lg:w-4/12 w-6/12">
  <div
    class="container p-8 rounded-lg shadow-lg"
  >
    <h2 class="text-xl font-bold text-white mb-2 text-center">We sent you a code.</h2>
    <p class="text-white text-center mb-4">
      Please, enter the code below to verify your email<br /><span
        class="text-theme-keith-highlight">{email}</span
      >
    </p>
    <div class="flex justify-center mb-6 space-x-2">
      {#each [0, 1, 2, 3, 4, 5] as _, index}
        <input
          id={"input-" + index}
          type="text"
          maxlength="1"
          class="text-white w-10 h-10 ring-1 ring-theme-keith-primary focus:ring-theme-keith-highlight focus:outline-1 focus:outline-none text-theme-keith-accentone text-xl rounded-lg text-center"
          bind:value={code[index]}
          on:input={(e) => handleInput(e, index)}
          on:keydown={(e) => handleInput(e, index)}
          required
        />
      {/each}
    </div>
    <Button
      on:click={verifyCode}
      class="w-full py-2 bg-theme-dark-primary text-theme-dark-white font-bold rounded hoverClass transition"
    >
      Verify
    </Button>
  </div>
</div>

<style>
  .container{
      background-image: linear-gradient(180deg,#181818, #001524 );
    }

    .hoverClass{
    background-image: #012431b1;
}
</style>
