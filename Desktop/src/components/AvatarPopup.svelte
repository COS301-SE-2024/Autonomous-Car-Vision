<script>
    import { createEventDispatcher } from 'svelte';
    import { Icon } from 'svelte-materialify';
    
    export let items = [];
    
  </script>
  
  <div class="bg-gray-dark text-white border border-white border-opacity-10 rounded-lg p-2 w-64 flex flex-col z-50">
    <nav>
      <ul class="list-none p-0 m-0">
        {#each items as { name, route, iconPath }}
          <li class="p-2 border-b border-opacity-10 border-white rounded-md hover:bg-blue-light transition">
            <a href={route} class="flex items-center text-inherit no-underline">
              <Icon path={iconPath}/>
              <span class="ml-2">{name}</span>
            </a>
          </li>
        {/each}
      </ul>
    </nav>
  </div>