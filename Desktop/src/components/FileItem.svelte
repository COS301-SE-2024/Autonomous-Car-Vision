<script>
    import { Icon } from "svelte-materialify";
    import { mdiCloseThick } from '@mdi/js';

    export let file;
    export let onRemove;
  
    function handleRemove() {
      onRemove(file);
    }
  </script>
  
  <div class="flex justify-between items-center border-gray-dark p-2 rounded-md mb-2 bg-gray-light">
    <span>{file.name}</span>
    <button on:click={handleRemove}>
        <Icon path={mdiCloseThick}/>
    </button>
  </div>