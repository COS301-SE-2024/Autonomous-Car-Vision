<script>
    import OnboardNewTeam from "../components/OnboardNewTeam.svelte";
    import {theme } from "../stores/themeStore";
</script>

{#if $theme === 'highVizLight'}
    <div class="min-h-screen lightScreen">
        <OnboardNewTeam />
        <!-- TODO: Add error success message depending after successful signUp -->
        <!-- TODO: Add back button -->
    </div>
{:else}
    <div class="min-h-screen">
        <OnboardNewTeam />
        <!-- TODO: Add error success message depending after successful signUp -->
        <!-- TODO: Add back button -->
    </div>
{/if}

<style>
    .lightScreen {
        background-image: linear-gradient(180deg, #F8F8F8, #B6D9E8);
   }
   </style>