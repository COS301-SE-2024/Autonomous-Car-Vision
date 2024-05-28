<script>

import navigate from 'svelte-spa-router'

const onSubmit = () => {
    console.log("Login button clicked")
    console.log(document.getElementsByName('uName-Email').value)
    console.log(document.getElementById('uname-email').value)

    console.log(document.getElementById('password').value)

}

</script>

<div class="w-10/12 mx-auto py-4 my-4">
    <div class="grid grid-cols-2 place-items-center w-full gap-2">
        <div class="w-full">
            <a href="#/signup" on:click={() => navigate("/signup")}>
                <button class="bg-green-400 w-8/12 rounded-lg">Sign Up</button>
            </a>
        </div>
        <div class="w-full p-4 border-2 rounded-md border-green-500">
            <div class="text-left">
                <h1 class="text-2xl">
                    Welcome back!
                </h1>
                <p>
                    Please enter your information.
                </p>
            </div>
            <div id="form" class="flex flex-col gap-1 py-2">
                <!-- <label for="uName-Email">Username or Email</label> -->
                <input type="text" id="uname-email" name="uName-Email" placeholder="Username or Email" />
                <!-- <label for="uName-Email">Password</label> -->
                <input type="password" id="password" name="password" placeholder="Password..." />
            </div>
            <button class="w-full p-1 my-2 bg-blue-500 rounded-md" on:click={onSubmit}>Log in</button>
        </div>
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