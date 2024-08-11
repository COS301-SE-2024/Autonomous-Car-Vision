<script>
    import { onMount } from "svelte";
    import { location } from "svelte-spa-router";
    import { Avatar, Icon } from "svelte-materialify";
    import {
        mdiViewGallery,
        mdiUpload,
        mdiCloudPrintOutline,
        mdiHelpCircle,
        mdiAccountCog,
        mdiLogout,
        mdiEyeRefresh,
        mdiAccountGroup,
        mdiAccountCheckOutline,
        mdiLanPending,
        mdiChevronUp,
        mdiChevronDown,
    } from "@mdi/js";

    import AccountPopup from "./AccountPopup.svelte";

    export let width;

    let username = "Username";
    let name = "User Name";
    let profileImg =
        "https://media.contentapi.ea.com/content/dam/ea/f1/f1-23/common/articles/patch-note-v109/pj-f123-bel-w01-rus.jpg.adapt.1456w.jpg";

    let showAccountPopup = false;
    let showTeamDropdown = false; 

    let routes = [
        {
            name: "Team",
            iconPath: mdiAccountGroup,
            subRoutes: [  // Subroutes for the Team dropdown
                {
                    name: "Team View",
                    route: "#/team",
                    iconPath: mdiAccountCheckOutline,
                },
                {
                    name: "Team Network",
                    route: "#/team/network",
                    iconPath: mdiLanPending,
                },
            ]
        },
        {
            name: "Visualizer",
            route: "#/visualize",
            iconPath: mdiEyeRefresh,
        },
        {
            name: "Gallery",
            route: "#/gallery",
            iconPath: mdiViewGallery,
        },
        {
            name: "Upload",
            route: "#/upload",
            iconPath: mdiUpload,
        },
        {
            name: "Models",
            route: "#/models",
            iconPath: mdiCloudPrintOutline,
        },
        {
            name: "Help",
            route: "#/help",
            iconPath: mdiHelpCircle,
        },
    ];

    const accountPopupItems = [
        {
            name: "Account settings",
            route: "#/accountsettings",
            iconPath: mdiAccountCog,
        },
        { name: "Log out", route: "#/", iconPath: mdiLogout },
    ];

    function toggleAccountPopup() {
        showAccountPopup = !showAccountPopup;
        console.log("TOGGLE: ", showAccountPopup);
    }

    function closeAccountPopup() {
        showAccountPopup = false;
    }

    function toggleTeamDropdown() {
        showTeamDropdown = !showTeamDropdown;
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
        document.addEventListener("click", handleClickOutside);

        return () => {
            document.removeEventListener("click", handleClickOutside);
        };
    });
</script>

<div
    class="sidebarV2 h-full w-auto bg-theme-dark-background text-white flex flex-col justify-end"
>
    {#each routes as route}
        <div class="nav-item {'#' + $location === route.route ? 'active' : ''}">
            {#if route.subRoutes}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="w-full flex justify-start gap-2 items-center cursor-pointer" on:click={toggleTeamDropdown}>
                    <Icon path={route.iconPath} />
                    {#if width >= 150}
                        <span class="ml-2">
                            {route.name}
                        </span>
                    {/if}
                    <Icon path={showTeamDropdown ? mdiChevronUp : mdiChevronDown} />
                </div>
            {:else}
            <a class="w-full" href={route.route} on:click={route.subRoutes ? toggleTeamDropdown : undefined}>
                <div class="flex justify-start gap-2 items-center">
                    <Icon path={route.iconPath} />
                    {#if width >= 150}
                        <span class="ml-2">
                            {route.name}
                        </span>
                    {/if}
                    {#if route.subRoutes}
                        <Icon path={showTeamDropdown ? mdiChevronUp : mdiChevronDown} />
                    {/if}
                </div>
            </a>

            {/if}
        </div>
        {#if route.subRoutes && showTeamDropdown}
            <div class="sub-routes ml-8">
                {#each route.subRoutes as subRoute}
                    <div class="sub-nav-item {'#' + $location === subRoute.route ? 'active' : ''}">
                        <a class="w-full" href={subRoute.route}>
                            <div class="flex justify-start gap-2 items-center">
                                    <Icon path={subRoute.iconPath} />
                                {#if width >= 150}
                                    <span class="ml-0.5">
                                        {subRoute.name}
                                    </span>
                                {/if}
                            </div>
                        </a>
                    </div>
                {/each}
            </div>
        {/if}
    {/each}
        <div
            class="relative cursor-pointer avatar-container m-3 grid {width < 150 ? 'place-items-center' : ''}"
            on:click={toggleAccountPopup}
            on:keydown
        >
            <div
                style="width: {width < 150 ? 'fit-content' : 'auto'};"
                class="{'/accountsettings' === $location ||
                '/changepassword' === $location
                    ? 'bg-dark-background'
                    : ''} lg:bg-dark-background_secondary hover:bg-dark-background p-1 flex justify-start gap-2 items-center rounded-full"
            >
                <Avatar
                    size="34px"
                    class="bg-gray rounded-full content-center w-fit"
                >
                    <img class="accountImg" src={profileImg} alt="img" />
                </Avatar>
                {#if width >= 150}
                    <div class="w-auto flex flex-col justify-start items-center">
                        <span class="w-fit text-left text-xs font-bold"
                            >{username}</span
                        >
                        <span class="w-fit text-left text-xs">{name}</span>
                    </div>
                {/if}   
            </div>
        </div>
        {#if showAccountPopup}
            <div
                class="popupAcc z-20 mt-2 account-popup-content" style="left: {width + 10}px;"
            >
                <AccountPopup items={accountPopupItems} on:close={closeAccountPopup} />
            </div>
        {/if}
</div>

<style>
    .popupAcc {
        position: absolute;
    }

    .sidebarV2 {
        border-radius: 15px;
        overflow: hidden;
    }

    .nav-item, .sub-nav-item {
        display: flex;
        justify-content: start;
        padding: 10px 0 10px 20px;
    }

    .nav-item > a > div {
        opacity: 0.5;
    }

    .nav-item > a > div:hover, .sub-nav-item > a > div:hover {
        color: aliceblue;
        opacity: 1;
        font-weight: 600;
        transition: opacity 0.5s;
    }

    .active > a > div {
        opacity: 1;
        color: white;
        font-weight: 600;
    }

    .sub-routes {
        display: flex;
        flex-direction: column;
    }

    .accountImg {
        width: 100%;
    }
</style>
