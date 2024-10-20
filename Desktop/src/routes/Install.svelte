<script>
    import InstallerGuide from "../components/InstallerGuide.svelte";
    import { theme } from "../stores/themeStore";
</script>

{#if $theme === "highVizLight"}
    <div class="lightScreen">
        <InstallerGuide />
    </div>
{:else}
    <div class="darkScreen">
        <InstallerGuide />
    </div>
{/if}

<!--  -->

<style>
    .lightScreen {
        background-image: linear-gradient(180deg, #f8f8f8, #b6d9e8);
        height: 100%;
    }

    .darkScreen {
        background-image: linear-gradient(0deg,#181818, #001524);
        height: 100%;
    }
</style>
