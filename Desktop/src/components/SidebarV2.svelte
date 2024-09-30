<script>
    import { onMount } from "svelte";
    import { location } from "svelte-spa-router";
    import { Avatar, Icon } from "svelte-materialify";
    import {
        mdiViewGallery,
        mdiCloudPrintOutline,
        mdiHelpCircle,
        mdiAccountCog,
        mdiLogout,
        mdiCar,
        mdiEyeRefresh,
        mdiAccountGroup,
        mdiAccountCheckOutline,
        mdiLanPending,
        mdiChevronUp,
        mdiChevronDown,
        mdiPipeDisconnected,
        mdiSecurity,
    } from "@mdi/js";
    import axios from "axios";
    import CryptoJS from 'crypto-js';

    import ThemeToggler from "./ThemeToggler.svelte";
    import {theme } from "../stores/themeStore";


    import AccountPopup from "./AccountPopup.svelte";

    export let width;

    let username = "";
    let name = "";
    let profileImg = "";

    let showAccountPopup = false;
    let showTeamDropdown = false; 

    let HOST_IP;

    let routes = [
        {
            id: "extend-teams",
            name: "Team",
            iconPath: mdiAccountGroup,
            subRoutes: [  // Subroutes for the Team dropdown
                {
                    id: "go-to-teams-view",
                    name: "Team View",
                    route: "#/teamView",
                    iconPath: mdiAccountCheckOutline,
                },
                {
                    id: "go-to-teams-network",
                    name: "Team Network",
                    route: "#/teamNetwork",
                    iconPath: mdiLanPending,
                },
            ]
        },
//         {
//             id: "go-to-visualizer",
//             name: "Visualizer",
//             route: "#/visualize",
//             iconPath: mdiEyeRefresh,
//         },
        {
            id: "go-to-drive-gallery",
            name: "Drive Gallery",
            route: "#/drivegallery",
            iconPath: mdiCar,
        },
        {
            id: "go-to-pipes",
            name: "Pipes",
            route: "#/svelvet",
            iconPath: mdiPipeDisconnected,
        },
        {
            id: "go-to-gallery",
            name: "Gallery",
            route: "#/gallery",
            iconPath: mdiViewGallery,
        },
        {
            id: "go-to-models",
            name: "Models",
            route: "#/models",
            iconPath: mdiCloudPrintOutline,
        },
        {
             id: "go-to-help",
            name: "Help",
            route: "#/help",
            iconPath: mdiHelpCircle,
        },
    ];

    const accountPopupItems = [
        {
            id: "go-to-tests",
            name: "Privacy & Security",
            route: "#/tests",
            iconPath: mdiSecurity,
        },
        {
            id: "go-to-account-settings",
            name: "Account settings",
            route: "#/accountsettings",
            iconPath: mdiAccountCog,
        },
        { 
            id: "go-to-logout",
            name: "Log out", 
            route: "#/", 
            iconPath: mdiLogout },
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

    onMount(async () => {
         HOST_IP = await window.electronAPI.getHostIp();
        document.addEventListener("click", handleClickOutside);

        // Get user data with uid
        axios
            .post("http://" + HOST_IP + ":8000/getUserData/", {
                uid: window.electronAPI.getUid(),
            })
            .then(async (response) => {
                username = response.data.uname;
                name = response.data.uemail;
                    
                let profileEmail = response.data.uemail;
                profileEmail = profileEmail.trim().toLowerCase();
                // const emailHash = profileEmail;

                
                const emailHash = CryptoJS.SHA256(profileEmail);
                profileImg = `https://www.gravatar.com/avatar/${emailHash}?d=retro`;
                console.log(profileImg);
            })
            .catch((error) => {
                console.error("Error fetching user data:", error);
                // Set a default image in case of error
                profileImg = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=retro";
            });

        return () => {
            document.removeEventListener("click", handleClickOutside);
        };
    });
</script>

{#if $theme === 'highVizLight'}
<div
    class="sidebarV2Light h-full w-auto text-black flex flex-col justify-end"
>
    {#each routes as route}
        <div class="nav-itemLight {'#' + $location === route.route ? 'activeLight' : ''}">
            {#if route.subRoutes}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <div class="w-full opacity-50 flex justify-start gap-2 items-center cursor-pointer" on:click={toggleTeamDropdown}>
                    <Icon path={route.iconPath} id={route.id}/>
                    {#if width >= 150}
                        <span class="ml-2">
                            {route.name}
                        </span>
                    {/if}
                    <Icon path={showTeamDropdown ? mdiChevronUp : mdiChevronDown} />
                </div>
            {:else}
            <a class="w-full" id={route.id} href={route.route} on:click={route.subRoutes ? toggleTeamDropdown : undefined}>
                <div class="flex justify-start gap-2 items-center">
                    <Icon path={route.iconPath} id={route.id}/>
                    {#if width >= 150}
                        <span class="ml-2">
                            {route.name}
                        </span>
                    {/if}
                    {#if route.subRoutes}
                        <Icon path={showTeamDropdown ? mdiChevronUp : mdiChevronDown} id={route.id}/>
                    {/if}
                </div>
            </a>

            {/if}
        </div>
        {#if route.subRoutes && showTeamDropdown}
            <div class="sub-routes ml-8">
                {#each route.subRoutes as subRoute}
                    <div class="sub-nav-itemLight {'#' + $location === subRoute.route ? 'activeLight' : ''}">
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
                    ? 'bg-highVizLight-background'
                    : ''} lg:bg-highVizLight-background_secondary hover:bg-highVizLight-background p-1 flex justify-start gap-2 items-center rounded-full"
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
{:else}
<div
class="sidebarV2 h-full w-auto bg-theme-dark-background text-white flex flex-col justify-end"
>
{#each routes as route}
    <div class="nav-item {'#' + $location === route.route ? 'active' : ''}">
        {#if route.subRoutes}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="w-full opacity-70 flex justify-start gap-2 items-center cursor-pointer" on:click={toggleTeamDropdown}>
                <Icon path={route.iconPath} id={route.id}/>
                {#if width >= 150}
                    <span class="ml-2">
                        {route.name}
                    </span>
                {/if}
                <Icon path={showTeamDropdown ? mdiChevronUp : mdiChevronDown} id={route.id}/>
            </div>
        {:else}
        <a class="w-full" id={route.id} href={route.route} on:click={route.subRoutes ? toggleTeamDropdown : undefined}>
            <div class="flex justify-start gap-2 items-center">
                <Icon path={route.iconPath} id={route.id}/>
                {#if width >= 150}
                    <span class="ml-2">
                        {route.name}
                    </span>
                {/if}
                {#if route.subRoutes}
                    <Icon path={showTeamDropdown ? mdiChevronUp : mdiChevronDown} id={route.id}/>
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
{/if}



<style>
    .popupAcc {
        position: absolute;
    }

    .sidebarV2 {
        border-radius: 15px;
        overflow: hidden;
    }

    .sidebarV2Light {
        border-radius: 15px;
        overflow: hidden;
        background: #B6D9E8;
    }

    .nav-item, .sub-nav-item {
        display: flex;
        justify-content: start;
        padding: 10px 0 10px 20px;
    }

    .nav-item > a > div, .sub-nav-item > a > div{
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
        border-right: solid 4px white;
    }

     .nav-itemLight > a > div:hover, .sub-nav-itemLight > a > div:hover {
        color: #007ACC;
        opacity: 1;
        font-weight: 600;
        transition: opacity 0.5s;
    }

     .nav-itemLight, .sub-nav-itemLight {
        display: flex;
        justify-content: start;
        padding: 10px 0 10px 20px;
    }

     .nav-itemLight > a > div, .sub-nav-itemLight > a > div{
        opacity: 0.5;
    }
    .activeLight > a > div {
        opacity: 1;
        color: #2a8fbb;
        font-weight: 600;
        border-right: solid 4px #2a8fbb;
    }


    .sub-routes {
        display: flex;
        flex-direction: column;
    }

    .accountImg {
        width: 100%;
    }
</style>