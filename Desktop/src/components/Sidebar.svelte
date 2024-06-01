<script>
  import { onMount } from "svelte";
  import { Avatar, Icon } from "svelte-materialify";
  import { mdiAccountCircle } from "@mdi/js";
  import { mdiAccountCog } from "@mdi/js";
  import { mdiLogout } from "@mdi/js";

  import AccountPopup from "./AccountPopup.svelte";

  export let items = [];

  const accountPopupItems = [
    {
      name: "Account settings",
      route: "#/accountsettings",
      iconPath: mdiAccountCog,
    },
    { name: "Log out", route: "#/", iconPath: mdiLogout },
  ];

  let showAccountPopup = false;

  function toggleAccountPopup() {
    showAccountPopup = !showAccountPopup;
  }

  function closeAccountPopup() {
    showAccountPopup = false;
  }

  onMount(() => {
    document.addEventListener("click", handleClickOutside);
  });

  function handleClickOutside(event) {
    const popup = document.querySelector(".account-popup-content");
    const avatar = document.querySelector(".avatar-container");
    if (popup && !popup.contains(event.target) && !avatar.contains(event.target)) {
      closeAccountPopup();
    }
  }
</script>

<div class="fixed h-screen w-1/5 bg-gray-dark p-4 flex flex-col justify-end text-gray-light z-50">
  <aside>
    <nav>
      <ul class="flex flex-col space-y-2">
        {#each items as { name, route, iconPath }}
          <li class="border-b border-gray-light">
            <a href={route} class="flex items-center py-2 hover:bg-gray transition">
              <Icon path={iconPath} />
              <span class="ml-2">{name}</span>
            </a>
          </li>
        {/each}
      </ul>
    </nav>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="relative flex justify-center items-center py-4 border-gray cursor-pointer avatar-container" on:click={toggleAccountPopup}>
      <Avatar class="bg-gray p-2 rounded-full">
        <Icon path={mdiAccountCircle} />
      </Avatar>
      {#if showAccountPopup}
        <div class="absolute top-0 right-0 transform translate-x-full -translate-y-full mt-2 account-popup-content">
          <AccountPopup items={accountPopupItems} on:close={closeAccountPopup}/>
        </div>
      {/if}
    </div>
  </aside>
</div>