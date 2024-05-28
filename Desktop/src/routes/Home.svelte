<script>
    import navigate from "svelte-spa-router";
</script>

<div>
    <h1 class="text-4xl text-center">Home</h1>
    <div class="flex flex-col gap-4 justify-center content-center flex-wrap">
        <a href="#/login" on:click={() => navigate("/login")}>
            <button class="bg-green-400 w-20 rounded-lg">Log In</button>
        </a>
        <a href="#/signup" on:click={() => navigate("/signup")}>
            <button class="bg-green-400 w-20 rounded-lg">Sign Up</button>
        </a>
    </div>
</div>
