<script>
    import { Button, MaterialApp } from "svelte-materialify";
</script>

<MaterialApp>
    <div>
        <h1 class="text-4xl text-center">Home</h1>
        <div
            class="flex flex-col gap-4 justify-center content-center flex-wrap"
        >
            <a href="#/login">
                <Button depressed class="bg-primary-green-light w-20 rounded-lg">Log In</Button>
            </a>
            <a href="#/signup">
                <Button depressed class="bg-primary-green-light w-20 rounded-lg">Sign Up</Button>
            </a>
        </div>
    </div>
</MaterialApp>
