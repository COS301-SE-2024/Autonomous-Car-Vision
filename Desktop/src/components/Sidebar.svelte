<script>
    import { Avatar, Icon } from "svelte-materialify";
    import { mdiAccountCircle } from "@mdi/js";
    import { mdiAccountCog } from "@mdi/js";
    import { mdiLogout } from "@mdi/js";
  
    // import AccountPopup from "./AccountPopup.svelte";
  
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
  </script>
  
  <div class="fixed h-screen w-1/5 bg-gray-800 p-4 flex flex-col justify-end text-white">
    <aside>
      <nav>
        <ul class="flex flex-col space-y-2">
          {#each items as { name, route, iconPath }}
            <li class="border-t border-gray-700">
              <a href={route} class="flex items-center py-2 hover:bg-blue-600 transition">
                <Icon path={iconPath} />
                <span class="ml-2">{name}</span>
              </a>
            </li>
          {/each}
        </ul>
      </nav>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="flex justify-center items-center py-4 border-b border-gray-700 cursor-pointer" on:click={toggleAccountPopup}>
        <Avatar class="bg-gray-700 p-2 rounded-full">
          <Icon path={mdiAccountCircle} />
        </Avatar>
      </div>
      {#if showAccountPopup}
        <AccountPopup items={accountPopupItems}/>
      {/if}
    </aside>
  </div>