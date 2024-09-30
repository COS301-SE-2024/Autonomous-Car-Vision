<script>
    import SignUpForm from "../components/SignUpForm.svelte";
    import { theme } from "../stores/themeStore";
</script>

{#if $theme === "highVizLight"}
    <div class="min-h-screen lightScreen">
        <SignUpForm />
        <!-- TODO: Add error success message depending after successful signUp -->
        <!-- TODO: Add back button -->
    </div>
{:else}
    <div class="min-h-screen darkScreen">
        <SignUpForm />
        <!-- TODO: Add error success message depending after successful signUp -->
        <!-- TODO: Add back button -->
    </div>
{/if}

<style>
    .lightScreen {
        background-image: linear-gradient(180deg, #f8f8f8, #b6d9e8);
    }

    .darkScreen {
        background-image: linear-gradient(180deg, #001524, #181818);
    }
</style>
