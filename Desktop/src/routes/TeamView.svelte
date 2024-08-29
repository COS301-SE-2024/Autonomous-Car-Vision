<script>
    import TeamMember from '../components/TeamMember.svelte';
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import {mdiAccountPlus} from "@mdi/js";
    import {Icon, Button} from "svelte-materialify";
    import AddMember from "../components/AddMember.svelte";
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { createEventDispatcher, onMount } from 'svelte';
    import axios from 'axios';

    let showAddPopup = false;

    const dispatch = createEventDispatcher();

    function closeAddPopup() {
        showAddPopup = false;
    }

    let teamName = '';

    onMount(async () => {
        try {
            const response = await axios.post('http://localhost:8000/getTeamName/', {
                uid: window.electronAPI.getUid(),
            });
            teamName = response.data.teamName;
            console.log(teamName);
        } catch (error) {
            console.error(error);
        }
        });

        let users = [];

        onMount(async () => {
        try {
            const response = await axios.post('http://localhost:8000/getTeamMembers/', {
            uid: window.electronAPI.getUid(),
            });
            users = response.data.teamMembers;
        } catch (error) {
            console.error(error);
        }
        });     
</script>

<ProtectedRoutes>
    {#if $isLoading}
        <div class="flex justify-center w-full">
        <Spinner />
        </div>
    {:else}
        <div class="user-list text-theme-dark-lightText">
            <div class="header text-xl items-center text-center">
                <h2>{teamName}</h2>
            </div>
            <div class="flex text-white flex-row space-between">
                <h3 class="px-5">Active Members</h3>
                <Button on:click={() => (showAddPopup = true)} class="ml-96 rounded cursor-pointer bg-theme-dark-background hover:bg-theme-dark-background transition-all duration-300 ease-in-out"><Icon path={mdiAccountPlus} class="px-2"/> Invite Member</Button> 
            </div>
            <input
                type="text"
                placeholder="Search..."
                class="bg-theme-dark-white text-black rounded-lg border-2 border-theme-dark-secondary p-2 w-full border-solid text-lg"
            />
            <div class="grid grid-cols-4 mt-3 border rounded-lg border-gray-dark align-center items-center px-3 py-3 text-white">
                <div class="flex items-center col-span-2"> <p class="ml-6">Name</p>
                </div>
                <p>Role</p>
                <p>Last Active</p>
            </div>
            {#each users as user}
                <TeamMember
                    uid={user.uid}
                    name={user.uname}
                    email={user.uemail}
                    role={user.is_admin === true ? "Admin" : "Member"}
                    lastActivity={"We do not store this data yet"}
                    profilePhoto={"https://i.pravatar.cc/150?img=1"}
                    
                />
            {/each}
        </div>
     {/if}

     {#if showAddPopup}
    <AddMember
      on:cancel={closeAddPopup}
      on:save={closeAddPopup}
    />
  {/if}
</ProtectedRoutes>

<style>
    .user-list {
        width: 100%;
        max-width: 750px;
        margin: 0 auto;
    }
    .header {
        color: white;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        /* margin-left: 10px; */
    }
</style>
