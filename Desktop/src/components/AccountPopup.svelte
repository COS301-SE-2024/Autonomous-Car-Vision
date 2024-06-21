<script>
  import { createEventDispatcher } from "svelte";
  import { Icon } from "svelte-materialify";

  export let items = [];

  const dispatch = createEventDispatcher();

  function handleOptionClick() {
    dispatch("close");
  }
</script>

<div
  class="bg-theme-dark-white text-theme-dark-backgroundBlue border-1 border-theme-dark-backgroundBlue border-opacity-10 rounded-lg p-2 w-64 flex flex-col z-50"
>
  <nav>
    <ul class="list-none p-0 m-0">
      {#each items as { name, route, iconPath }}
        <li
          class="p-2 border-b border-opacity-10 border-theme-dark-backgroundBlue rounded-md hover:bg-theme-dark-backgroundBlue hover:text-theme-dark-white transition"
        >
          <a href={route} class="flex items-center text-inherit no-underline">
            <Icon path={iconPath} />
            <span class="ml-2">{name}</span>
          </a>
        </li>
      {/each}
    </ul>
  </nav>
</div>
