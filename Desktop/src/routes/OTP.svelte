<script>
    let email = "";
    export let code = "";
  
    function verifyCode() {
      alert(`Verifying code: ${code}`);
      console.log("Code: " + code)
    }
  
    function updateCode(index, value) {
      code = code.substring(0, index) + value + code.substring(index + 1);
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
  
  <div class="flex items-center justify-center min-h-screen bg-white">
    <div class="bg-white p-8 rounded-lg shadow-lg border border-theme-keith-accentone">
      <h2 class="text-xl font-bold mb-2 text-center">
        We sent you a code.
      </h2>
      <p class="text-black text-center mb-4">
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
            class="w-10 h-10 ring-1 ring-theme-keith-primary focus:ring-theme-keith-highlight focus:outline-1 focus:outline-none text-black text-xl rounded-lg text-center"
            bind:value={code[index]}
            on:input={(e) => handleInput(e, index)}
            on:keydown={(e) => handleInput(e, index)}
            required
          />
        {/each}
      </div>
      <button
        on:click={verifyCode}
        class="w-full py-2 bg-theme-keith-accentone font-bold rounded hover:bg-theme-keith-accenttwo transition"
      >
        Verify
      </button>
    </div>
  </div>
  
  <style>
  </style>
  