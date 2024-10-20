<script>
    import OnboardJoin from "../components/OnboardJoin.svelte";
    import {theme } from "../stores/themeStore";
</script>

{#if $theme === 'highVizLight'}
    <div class="min-h-screen lightScreen">
        <OnboardJoin />
    </div>
{:else}
    <div class="min-h-screen">
        <OnboardJoin />
    </div>
{/if}

<style>
    .lightScreen {
        background-image: linear-gradient(180deg, #F8F8F8, #B6D9E8);
   }
   </style>