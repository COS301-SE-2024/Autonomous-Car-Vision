<script>
    import TeamMember from '../components/TeamMember.svelte';
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import {mdiAccountPlus} from "@mdi/js";
    import {Icon, Button} from "svelte-materialify";

    const users = [
        {
            name: 'Felix',
            email: 'felix@miro.com',
            role: 'Member',
            license: 'Full',
            lastActivity: '-'
        },
        {
            name: "Alice",
            email: "alice@example.com",
            role: "Admin",
            license: "Full",
            lastActivity: "2023-09-15"
        },
        {
            name: "Bob",
            email: "bob@example.com",
            role: "Member",
            license: "Trial",
            lastActivity: "2023-09-10"
        }
        // Add more user objects here as needed
    ];
</script>

<ProtectedRoutes>
    <div class="user-list text-theme-dark-lightText">
        <div class="header text-xl items-center text-center">
            <h2>Team Name</h2>
        </div>
        <div class="flex text-white flex-row space-between">
            <h3 class="px-5">Active Members</h3>
            <Button class="ml-96 rounded cursor-pointer bg-theme-dark-background hover:bg-theme-dark-background transition-all duration-300 ease-in-out"><Icon path={mdiAccountPlus} class="px-2"/> Invite Member</Button> 
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
                name={user.name}
                email={user.email}
                role={user.role}
                lastActivity={user.lastActivity}
                
            />
        {/each}
    </div>
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
