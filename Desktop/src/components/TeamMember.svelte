<script>
  import { mdiMinusBox, mdiDelete } from "@mdi/js";
  import { Icon, Button, Avatar } from "svelte-materialify";
  import RemoveMember from "./RemoveMember.svelte";
  import { theme } from "../stores/themeStore";

  export let name;
  export let role;
  export let email;
  export let lastActivity;
  export let profilePhoto;
  export let uid;

  let showRemovePopup = false;

  function closeRemovePopup() {
    showRemovePopup = false;
  }

</script>

{#if $theme === "highVizLight"}
  <div
    class="grid grid-cols-4 border-b shadow-card border-gray-dark align-center items-center px-3 py-6"
  >
    <div class="flex items-center col-span-2">
      <Button
        on:click={() => (showRemovePopup = true)}
        class="text-red border-none rounded cursor-pointer px-0"
      >
        <Icon path={mdiMinusBox} /></Button
      >
      <img src={profilePhoto} alt={name} class="user-avatar px-2" size="2rem" />
      <div class="flex flex-col text-black">
        <div class="text-bold">{name}</div>
        <div class="user-email">{email}</div>
      </div>
    </div>
    <div class="user-role text-black">{role}</div>
    <div class="user-last-activity text-black">{lastActivity}</div>
    {#if showRemovePopup}
      <RemoveMember on:cancel={closeRemovePopup} on:save={closeRemovePopup} role={role} />
    {/if}
  </div>
{:else}
  <div
    class="grid grid-cols-4 border-b shadow-card border-gray-dark text-white align-center items-center px-3 py-6"
  >
    <div class="flex items-center col-span-2">
      <Button
        on:click={() => (showRemovePopup = true)}
        class="text-red border-none rounded cursor-pointer px-0"
      >
        <Icon path={mdiMinusBox} /></Button
      >
      <img src={profilePhoto} alt={name} class="user-avatar px-2" size="2rem" />
      <div class="flex flex-col text-white">
        <div class="text-bold">{name}</div>
        <div class="user-email">{email}</div>
      </div>
    </div>
    <div class="user-role text-white">{role}</div>
    <div class="user-last-activity text-white">{lastActivity}</div>
    {#if showRemovePopup}
      <RemoveMember
        {uid}
        on:cancel={closeRemovePopup}
        on:save={closeRemovePopup}
      />
    {/if}
  </div>
{/if}

<style>
  .user-avatar {
    border-radius: 50%;
    margin-right: 10px;
  }

  .user-email {
    text-overflow: ellipsis;
  }
</style>
