<script>
    import InstallerGuide from "../components/InstallerGuide.svelte";
    import {theme } from "../stores/themeStore";
</script>

{#if $theme === 'highVizLight'}
    <div class="min-h-screen lightScreen">
        <InstallerGuide />
        <!-- TODO: Add error success message depending after successful signUp -->
        <!-- TODO: Add back button -->
    </div>
{:else}
    <div class="min-h-screen">
        <InstallerGuide />
        <!-- TODO: Add error success message depending after successful signUp -->
        <!-- TODO: Add back button -->
    </div>
{/if}

<style>
    .lightScreen {
        background-image: linear-gradient(180deg, #F8F8F8, #B6D9E8);
   }
   </style><!--  -->