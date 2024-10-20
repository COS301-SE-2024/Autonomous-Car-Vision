<script>
    import OnboardNewTeam from "../components/OnboardNewTeam.svelte";
    import {theme } from "../stores/themeStore";
</script>

{#if $theme === 'highVizLight'}
    <div class="min-h-screen lightScreen">
        <OnboardNewTeam />
    </div>
{:else}
    <div class="min-h-screen">
        <OnboardNewTeam />
    </div>
{/if}

<style>
    .lightScreen {
        background-image: linear-gradient(180deg, #F8F8F8, #B6D9E8);
   }
   </style>