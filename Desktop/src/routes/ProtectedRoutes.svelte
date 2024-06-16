<!-- src/routes/ProtectedRoute.svelte -->
<script>
  import { token } from "../stores/auth";
  import { onMount } from "svelte";
  import { navigate } from "@sveltejs/kit/navigation"; // If using SvelteKit for navigation
  import Sidebar from "../components/Sidebar.svelte";

  import { isLoading } from "../stores/loading";
  import Spinner from "../components/Spinner.svelte";

  let data = null;

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

  onMount(async () => {
    isLoading.set(true);
    try {
      // Simulate data fetching with a delay
      await new Promise((resolve) => setTimeout(resolve, 3000));
      data = await fetchData();
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      isLoading.set(false);
    }
  });

  async function fetchData() {
    // Replace with your actual data fetching logic
    return { message: "Data loaded successfully" };
  }
</script>

<!-- Slot to render the protected content if authenticated -->

<div class="flex">
  <div class="w-1/5">
    <Sidebar />
  </div>
  {#if $isLoading}
    <Spinner />
  {/if}
  {#if data}
    <div class="flex-1 items-center p-4">
      <slot />
    </div>
  {/if}
</div>
