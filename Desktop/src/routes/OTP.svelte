<script>
    import axios from 'axios';
    import {push} from "svelte-spa-router";

    let email = "";
    let code = Array(6).fill("");

    const verifyCode = async () => {
        const otp = code.join('');
        console.log("Code: " + otp);
        console.log(localStorage.getItem('uid'))
        try {
            const response = await axios.post('http://localhost:8000/verifyOTP/', {
                'uid': localStorage.getItem('uid'),
                'otp': otp,
            });
            console.log(response);
            localStorage.setItem('token', JSON.stringify(response.data.token));
            push('/gallary');


        } catch (error) {
            console.error(error);
        }
    }

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

<div class="flex items-center justify-center min-h-screen bg-white">
    <div class="bg-white p-8 rounded-lg shadow-lg border border-gray">
        <h2 class="text-xl font-bold mb-2 text-center text-black">
            We sent you a code.
        </h2>
        <p class="text-black text-center mb-4">
            Please, enter the code below to verify your email<br/><span class="text-blue">{email}</span>
        </p>
        <div class="flex justify-center mb-6 space-x-2 text-black">
            {#each [0, 1, 2, 3, 4, 5] as _, index}
                <input
                        id={"input-" + index}
                        type="text"
                        maxlength="1"
                        class="w-10 h-10 ring-1 ring-blue focus:outline-1 focus:outline-gray-dark text-black text-xl rounded-lg text-center"
                        bind:value={code[index]}
                        on:input={(e) => handleInput(e, index)}
                        on:keydown={(e) => handleInput(e, index)}
                        required
                />
            {/each}
        </div>
        <button
                on:click={verifyCode}
                class="w-full py-2 bg-blue text-black font-bold rounded hover:bg-gray-light transition"
        >
            Verify
        </button>
    </div>
</div>

<style>
</style>
