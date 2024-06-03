<script>
    import { Button, MaterialApp } from "svelte-materialify";
</script>

<MaterialApp>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-xl w-80 border border-theme-keith-primary">
            <h1 class="text-4xl text-center mb-6 text-bold">Welcome to High-Viz</h1>
            <div class="flex flex-col gap-4 items-center">
                <a href="#/login" class="w-full">
                    <button class="w-full py-2 bg-theme-keith-accentone text-theme-keith-jet rounded-lg hover:bg-theme-keith-accenttwo transition">
                        Log In
                    </button>
                </a>
                <a href="#/signup" class="w-full">
                    <button class="w-full py-2 bg-theme-keith-accentone text-theme-keith-jet rounded-lg hover:bg-theme-keith-accenttwo transition">
                        Sign Up
                    </button>
                </a>
            </div>
        </div>
    </div>
</MaterialApp>