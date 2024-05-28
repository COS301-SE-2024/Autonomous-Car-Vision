<script>
    import navigate from "svelte-spa-router";

    const onSubmit = () => {
        console.log("Login button clicked");
        console.log(document.getElementsByName("uName-Email").value);
        console.log(document.getElementById("uname-email").value);

        console.log(document.getElementById("password").value);
        console.log(document.getElementById("Cpassword").value);

    };
</script>

<div class="w-10/12 mx-auto py-4 my-4">
    <div class="flex flex-row gap-2">
        <a
            class="w-full h-14 flex flex-col flex-wrap justify-center items-center bg-gray-200 rounded-sm"
            href="#/login"
            on:click={() => navigate("/login")}
        >
            <button>Log In</button>
        </a>
        <a
            class="w-full h-14 flex flex-col flex-wrap justify-center items-center bg-gradient-to-r from-green-300 to-green-600 rounded-sm"
            href="#/signup"
            on:click={() => navigate("/signup")}
        >
            <button>Sign Up</button>
        </a>
    </div>
    <div class="w-full p-4 border-2 rounded-md border-green-500 mt-2">
        <div class="text-left">
            <h1 class="text-2xl">Welcome!</h1>
            <p class="text-base">Please enter your information.</p>
            <p class="text-sm">Sign up with a username or email.</p>
        </div>
        <div id="form" class="flex flex-col gap-1 py-2">
            <!-- <label for="uName-Email">Username or Email</label> -->
            <input
                type="text"
                id="uname-email"
                name="uName-Email"
                placeholder="Username or Email"
            />
            <!-- <label for="uName-Email">Password</label> -->
            <input
                type="password"
                id="password"
                name="password"
                placeholder="Password..."
            />
            <input
                type="password"
                id="Cpassword"
                name="Cpassword"
                placeholder="Confirm password..."
            />
        </div>
        <button
            class="w-full p-1 my-2 bg-blue-500 rounded-md"
            on:click={onSubmit}>Register</button
        >
    </div>
</div>

<style>
    input {
        border-color: rgb(115, 255, 115);
        border-radius: 0.375rem;
        border: 2px solid rgb(115, 255, 115) !important;
        padding: 0.25rem;
    }

    input:focus {
        border: 2px solid rgb(115, 255, 115) !important;
    }
</style>
