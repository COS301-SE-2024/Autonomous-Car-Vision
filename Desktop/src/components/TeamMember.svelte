<script>

    import {mdiMinusBox} from "@mdi/js";
    import { Icon } from "svelte-materialify";
    export let name;
    export let role;
    export let email;
    export let lastActivity;
    let isRemoveOpen = false;

    function toggleRemove() {
        isRemoveOpen = !isRemoveOpen;
    }
</script>

<div class="grid grid-cols-4 border-b rounded-lg shadow-card border-gray-dark align-center items-center px-3 py-6">
    <div class="flex items-center col-span-2">
        <button class="red"> <Icon path={mdiMinusBox} /></button>
        <img src="https://via.placeholder.com/50" alt={name} class="user-avatar px-2"/>
        <div class="flex flex-col text-white">
            <div class="text-bold">{name}</div>
            <div class="user-email">{email}</div>
        </div>
    </div>
    <div class="user-role  text-white">{role}</div>
    <div class="user-last-activity  text-white">{lastActivity}</div>
    
</div>

<style>
    .user-avatar {
        border-radius: 50%;
        margin-right: 10px;
    }
</style>
