<script>
  import { createEventDispatcher } from "svelte";
  import { mdiDelete } from "@mdi/js";
  import { Icon } from "svelte-materialify";
  import axios from "axios";
  import { theme } from "../stores/themeStore";
  import { onMount } from "svelte";
  import toast from "svelte-french-toast";

  export let teamMember;
  export let role;
  export let uid;
  const dispatch = createEventDispatcher();

  let HOST_IP;
  onMount(async () => {
    HOST_IP = await window.electronAPI.getHostIp();
  });

  function closePopup() {
    dispatch("cancel");
  }

  function removeMember() {
    // make a post request to remove the member
    axios
      .post("http://" + HOST_IP + ":8000/removeMember/", {
        uid: window.electronAPI.getUid(),
        memberUid: uid,
      })
      .then((response) => {
        console.log(response);
        toast.success("Removed member successfully", {
          duration: 5000,
          position: "top-center",
        });
      })
      .catch((error) => {
        if (role != "Admin") {
          toast.error("You must be an admin to remove a member", {
            duration: 4000,
            position: "top-center",
          });
        } else {
          toast.error("Failed to remove member", {
            duration: 3000,
            position: "top-center",
          });
        }
        console.error(error);
      });
    dispatch("save");

    // remove the member with a post request
  }
</script>

{#if $theme === "highVizLight"}
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
          >
            <Icon path={mdiDelete} />
            Delete</button
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
          >
            <Icon path={mdiDelete} />
            Delete</button
          >
        </div>
      </div>
    </div>
  </div>
{/if}
