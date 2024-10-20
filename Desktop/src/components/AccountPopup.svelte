<script>
  import { createEventDispatcher } from "svelte";
  import { Icon } from "svelte-materialify";
  import { theme } from "../stores/themeStore";
  import ThemeToggler from "../components/ThemeToggler.svelte";

  export let items = [];

</script>

{#if $theme === "highVizLight"}
  <div
    class="relative bg-highVizLight-accent text-blac border border-highVizLight-background rounded-lg p-2 w-48 flex flex-col z-50"
  >
    <nav>
      <ul class="list-none p-0 m-0">
        {#each items as { name, route, iconPath }}
          <li
            class="p-2 border-b border-opacity-10 border-highVizLight-primary rounded-md hover:bg-theme-highVizLight-accent hover:text-white transition"
          >
            <a href={route} class="flex items-center text-inherit no-underline">
              <Icon path={iconPath} />
              <span class="ml-2">{name}</span>
            </a>
          </li>
        {/each}
        <li
          class="p-2 border-b border-opacity-10 border-highVizLight-primary rounded-md hover:bg-theme-highVizLight-accent hover:text-white transition"
        >
          <ThemeToggler />
        </li>
      </ul>
    </nav>
  </div>
{:else}
  <div
    class="relative bg-dark-background_secondary text-dark-primary border border-dark-background_secondary rounded-lg p-2 w-48 flex flex-col z-50"
  >
    <nav>
      <ul class="list-none p-0 m-0">
        {#each items as { name, route, iconPath }}
          <li
            class="p-2 border-b border-opacity-10 border-theme-dark-backgroundBlue rounded-md hover:bg-dark-background hover:text-theme-dark-white transition"
          >
            <a href={route} class="flex items-center text-inherit no-underline">
              <Icon path={iconPath} />
              <span class="ml-2">{name}</span>
            </a>
          </li>
        {/each}
        <li
          class="p-2 border-b border-opacity-10 border-highVizLight-primary rounded-md hover:bg-theme-highVizLight-accent hover:text-white transition"
        >
          <ThemeToggler />
        </li>
      </ul>
    </nav>
  </div>
{/if}
