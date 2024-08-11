<script>
    export let name;
    export let role;
    export let email;
    export let lastActivity;
    let isRemoveOpen = false;

    function toggleRemove() {
        isRemoveOpen = !isRemoveOpen;
    }
</script>

<div class="grid grid-cols[auto_1fr_auto_auto_auto] border-b-[11px_solid_#ccc] align-center items-center px-[0] py-[10px]">
    <div class="flex items-center">
        <input type="checkbox" />
        <img src="https://via.placeholder.com/50" alt={name} class="user-avatar"/>
        <div class="flex flex-col text-white">
            <div class="text-bold">{name}</div>
            <div class="user-email">{email}</div>
        </div>
    </div>
    <div class="user-role">{role}</div>
    <div class="user-last-activity">{lastActivity}</div>
    
</div>

<style>
    .user-avatar {
        border-radius: 50%;
        margin-right: 10px;
    }
</style>
