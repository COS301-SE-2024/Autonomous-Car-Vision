<script>
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
  </script>
  
  <div class="sidebar-content">
    <aside>
      <nav>
        <ul>
          {#each items as { name, route, iconPath }}
            <li>
              <a href={route}>
                <Icon path={iconPath} />
                <span>{name}</span>
              </a>
            </li>
          {/each}
        </ul>
      </nav>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="avatar" on:click={toggleAccountPopup}>
        <Avatar class="user-avatar">
          <Icon path={mdiAccountCircle} />
        </Avatar>
      </div>
      {#if showAccountPopup}
        <AccountPopup items={accountPopupItems}/>
      {/if}
    </aside>
  </div>
  
  <style>
      aside {
        position: fixed;
        width: 20vw;
        height: 100vh;
        padding: 1em;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      nav ul {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
      }
      nav ul li {
        padding: 0.5em 0;
        border-bottom: solid rgba(255, 255, 255, 0.1) 0.05em;
      }
      nav ul li:hover {
        background-color: rgba(52, 152, 219, 0.5);
      }
      nav ul li a {
        color: inherit;
        text-decoration: none;
        display: flex;
        align-items: center;
      }
      nav ul li a span {
        margin-left: 0.5em;
      }
      .avatar {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1em 0;
        border-top: solid rgba(255, 255, 255, 0.1) 0.05em;
        cursor: pointer;
      }
      .user-avatar {
        background-color: #34495e;
        padding: 0.5em;
        border-radius: 50%;
      }
    </style>
  