<script>
  import { onMount } from "svelte";
  import { Avatar, Icon } from "svelte-materialify";
  import { mdiAccountCircle , mdiHelpCircle} from "@mdi/js";
  import { mdiAccountCog } from "@mdi/js";
  import { mdiLogout } from "@mdi/js";
  import { push, location } from "svelte-spa-router";

  import { mdiViewGallery, mdiUpload, mdiCloudPrintOutline } from "@mdi/js";

  import AccountPopup from "./AccountPopup.svelte";

  const items = [
    { name: "Help", route: "#/help", iconPath: mdiHelpCircle },
    { name: "Gallery", route: "#/gallery", iconPath: mdiViewGallery },
    { name: "Upload", route: "#/upload", iconPath: mdiUpload },
    { name: "Models", route: "#/models", iconPath: mdiCloudPrintOutline },
  ];

  let username = "Username";
  let Name = "User Name";

  const accountPopupItems = [
    {
      name: "Account settings",
      route: "#/accountsettings",
      iconPath: mdiAccountCog,
    },
    { name: "Log out", route: "#/", iconPath: mdiLogout },
  ];

  let showAccountPopup = false;
  let currentRoute = "";

  function toggleAccountPopup() {
    showAccountPopup = !showAccountPopup;
  }

  function closeAccountPopup() {
    showAccountPopup = false;
  }

  function updateCurrentRoute() {
    currentRoute = window.location.hash;
  }

  function handleClickOutside(event) {
    const popup = document.querySelector(".account-popup-content");
    const avatar = document.querySelector(".avatar-container");
    if (
      popup &&
      !popup.contains(event.target) &&
      !avatar.contains(event.target)
    ) {
      closeAccountPopup();
    }
  }

  onMount(() => {
    updateCurrentRoute();
    window.addEventListener("hashchange", updateCurrentRoute);
    document.addEventListener("click", handleClickOutside);

    return () => {
      window.removeEventListener("hashchange", updateCurrentRoute);
      document.removeEventListener("click", handleClickOutside);
    };
  });

  function navigate(route) {
    updateCurrentRoute();
    console.log(route);
    push(route);
  }

  function getMarkerPosition() {
    let route = $location.startsWith("/video/") || $location === "/accountsettings" || $location === "/changepassword" ? "/gallery" : $location;
    for (let i = 0; i < items.length; i++) {
      if (items[i].route === route) {
        console.log(route, i);
        return `translateY(calc(calc(50% / ${items.length}) * ${i}))`;
      }
    }
  }
</script>

<div
  class="fixed h-screen w-1/6 bg-theme-dark-backgroundBlue flex flex-col justify-end z-50 text-white"
>
  <div class="popup">
    <div class="tabs">
      {#each items as item, i}
        <input
          type="radio"
          id={"tab" + i}
          name="tab"
          checked={$location === item.route ||
            (item.route === "/gallery" && $location.startsWith("/video")) ||
            $location === "/accountsettings" || $location === "/changepassword"}
        />
        <label
          for={"tab" + i}
          on:keydown
          on:click={() => navigate(item.route)}
          class={$location === item.route ||
          (item.route === "/gallery" && ($location.startsWith("/video") || $location === "/accountsettings" || $location === "/changepassword"))
            ? "active"
            : ""}
        >
          <Icon path={item.iconPath} />
          <span class="sidebartext ml-2">{item.name}</span>
        </label>
      {/each}
      <div class="marker" style="transform: {getMarkerPosition()};">
        <div id="top"></div>
        <div id="bottom"></div>
      </div>
    </div>
  </div>
  <div
    class="relative flex justify-center gap-4 items-center mt-2 py-2 px-2 rounded transition hover:bg-theme-dark-bgHover border-theme-dark-primary cursor-pointer avatar-container"
    on:click={toggleAccountPopup}
    on:keydown
  >
    <Avatar class="bg-gray p-2 rounded-full">
      <Icon path={mdiAccountCircle} />
    </Avatar>
    <div class="flex flex-col">
      <span class="text-sm font-bold">{username}</span>
      <span class="text-sm">{Name}</span>
    </div>
    {#if showAccountPopup}
      <div
        class="absolute top-0 right-0 transform translate-x-full -translate-y-1/3 mt-2 account-popup-content"
      >
        <AccountPopup items={accountPopupItems} on:close={closeAccountPopup} />
      </div>
    {/if}
  </div>
</div>

<style>
  .popup {
    position: relative;
    bottom: 2rem;
    width: 100%;
    overflow: hidden;
    background-color: white;
  }

  label {
    font-size: 24px;
    font-weight: 700;
    cursor: pointer;
    color: rgb(255, 255, 255);
    opacity: 0.4;
    transition: opacity 0.4s ease-in-out;
    display: block;
    width: 100%;
    text-align: center;
    z-index: 100;
    user-select: none;
  }

  input[type="radio"] {
    display: none;
    width: 0;
  }

  input[type="radio"]:checked + label {
    opacity: 1;
    color: white;
  }

  label:hover,
  input[type="radio"]:checked + label {
    opacity: 1;
    color: rgb(165, 165, 165);
  }


  label,
  input[type="radio"] {
    opacity: 1;
    color: white;
  }

  input[type="radio"]:checked + label.active {
    color: black;
    opacity: 1;
  }

  /* input[type="radio"]:checked + label.active:hover {
    color: rgb(165, 165, 165);
    opacity: 1;
  } */

  .tabs {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    position: relative;
    gap: 6px;
  }

  .marker {
    position: absolute;
    width: 100%;
    height: 200%;
    display: flex;
    flex-direction: column;
    bottom: 0;
    left: 0;
    transition: transform 0.2s ease-in-out;
  }
  .marker #bottom,
  .marker #top {
    background-color: #0c003c;
    box-shadow: 32px 32px 48px #2e364315;
  }
  .marker #top {
    height: 50%;
    margin-bottom: auto;
    border-radius: 0 0 32px 0;
  }
  .marker #bottom {
    height: calc(50% - 43px);
    border-radius: 0 32px 0 0;
  }

  label.active {
    color: black;
  }
</style>
