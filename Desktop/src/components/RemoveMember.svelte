<script>
    import { createEventDispatcher } from "svelte";
    import {theme} from '../stores/themeStore';
  
    export let teamMember;
    const dispatch = createEventDispatcher();
  
    function closePopup() {
    dispatch("closePopup");
  }

    function removeMember() {
      dispatch("cancel");
    }
  
  </script>
  {#if $theme === 'highVizLight'}
  <div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
    <div
      class="bg-highVizLight-accent p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
    >
      <div class="flex flex-col boder border-theme-dark-backgroundBlue">
        <p class="text-md">
          Are you sure you would like to remove this member from your team?
        </p>
        <div class="flex mt-4 space-x-4">
          <button
            on:click={closePopup}
            class="font-medium bg-opacity-70 px-4 py-2 bg-highVizLight-secondary text-white rounded hover:bg-opacity-100 transition-all duration-300 ease-in-out"
            >Cancel</button
          >
          <button
            on:click={removeMember}
            class="font-medium bg-opacity-70 px-4 py-2 bg-highVizLight-error text-white rounded hover:bg-opacity-100 transition-all duration-300 ease-in-out"
            >Delete</button
          >
        </div>
      </div>
    </div>
  </div>
  {:else}
  <div class="fixed inset-0 flex items-center justify-center bg-modal z-50">
    <div
      class="bg-theme-dark-background p-6 rounded-lg shadow-lg border border-theme-keith-primary w-1/4"
    >
      <div class="flex flex-col boder border-theme-dark-backgroundBlue">
        <p class="text-md">
          Are you sure you would like to remove this member from your team?
        </p>
        <div class="flex mt-4 space-x-4">
          <button
            on:click={closePopup}
            class="font-medium px-4 py-2 bg-theme-dark-primary text-white rounded"
            >Cancel</button
          >
          <button
            on:click={removeMember}
            class="font-medium px-4 py-2 bg-theme-dark-error text-white rounded"
            >Delete</button
          >
        </div>
      </div>
    </div>
  </div>
  {/if}

  