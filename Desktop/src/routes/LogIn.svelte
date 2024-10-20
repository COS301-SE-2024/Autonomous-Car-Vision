<script>
  import LoginForm from "../components/LoginForm.svelte";
  import { theme } from "../stores/themeStore";
</script>

{#if $theme === "highVizLight"}
  <div class="min-h-screen lightScreen">
    <LoginForm />
  </div>
{:else}
  <div class="min-h-screen darkScreen">
    <LoginForm />
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
