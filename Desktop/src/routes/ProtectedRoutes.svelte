<!-- src/routes/ProtectedRoute.svelte -->
<script>
    import { token } from '../stores/auth';
    import { onMount } from 'svelte';
    import { goto } from '@sveltejs/kit/navigation'; // If using SvelteKit for navigation
  
    let authToken;
  
    // Subscribe to the token store to get the current authentication state
    $: token.subscribe(value => {
      authToken = value;
    });
  
    // On component mount, check the authentication state
    onMount(() => {
      if (!authToken) {
        // Redirect to the login page if the user is not authenticated
        goto('/login'); // Change this to your login route
      }
    });
  </script>
  
  <!-- Slot to render the protected content if authenticated -->
  <slot />