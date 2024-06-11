<!-- src/routes/ProtectedRoute.svelte -->
<script>
    import { token } from "../stores/auth";
    import { onMount } from "svelte";
    import { navigate } from "@sveltejs/kit/navigation"; // If using SvelteKit for navigation
    import Sidebar from "../components/Sidebar.svelte";

    let authToken;

    // Subscribe to the token store to get the current authentication state
    $: token.subscribe((value) => {
        authToken = value;
    });

    // On component mount, check the authentication state
    onMount(() => {
        if (!authToken) {
            // Redirect to the login page if the user is not authenticated
            navigate("#login"); // Change this to your login route
        }
    });
</script>

<!-- Slot to render the protected content if authenticated -->
<div class="flex">
    <div class="w-1/5">
        <Sidebar />
    </div>
    <div class="flex-1 items-center p-4">
        <slot />
    </div>
</div>
