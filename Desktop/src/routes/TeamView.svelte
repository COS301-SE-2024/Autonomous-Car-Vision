<script>
    import TeamMember from '../components/TeamMember.svelte';
    import ProtectedRoutes from './ProtectedRoutes.svelte';

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
    <div class="user-list">
        <div class="header">
            <h2>Active Members</h2>
        </div>
        {#each users as user}
            <TeamMember
                name={user.name}
                email={user.email}
                role={user.role}
                license={user.license}
                lastActivity={user.lastActivity}
            />
        {/each}
    </div>
</ProtectedRoutes>

<style>
    .user-list {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
    }
    .header {
        background-color: #2962FF;
        color: white;
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
</style>
