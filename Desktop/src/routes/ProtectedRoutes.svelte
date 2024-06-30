<!-- src/routes/ProtectedRoute.svelte -->
<script>
  import { token } from "../stores/auth";
  import { onMount } from "svelte";
  import { navigate } from "@sveltejs/kit/navigation"; // If using SvelteKit for navigation
  import Sidebar from "../components/Sidebar.svelte";
  import SidebarV2 from "../components/SidebarV2.svelte";

  let authToken;

  // Subscribe to the token store to get the current authentication state
  $: token.subscribe((value) => {
    authToken = window.electronAPI.getToken();
  });

  // On component mount, check the authentication state
  onMount(() => {
    if (!authToken) {
      // Redirect to the login page if the user is not authenticated
      navigate("#login"); // Change this to your login route
    }
  });

  let sidebarWidth = 200; // initial width of the sidebar
  const minOffset = 200;
  const maxOffset = 500;

  function handleMouseMove(event) {
    let offset = event.pageX;

    offset = offset < minOffset ? minOffset : offset;
    offset = offset > maxOffset ? maxOffset : offset;

    sidebarWidth = offset;
  }

  function handleMouseUp() {
    window.removeEventListener('mousemove', handleMouseMove);
    window.removeEventListener('mouseup', handleMouseUp);
  }

  function handleMouseDown() {
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  }

  onMount(() => {
    // Cleanup event listeners if the component is unmounted
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  });
</script>

<!-- Slot to render the protected content if authenticated -->
<div class="h-full w-full">
  <div class="side">
    <div class="sidebar" style="width: {sidebarWidth}px;">
      <SidebarV2 />
    </div>
  <div class="handle" on:mousedown={handleMouseDown}></div>
  </div>
  <div class="content" style="margin-left: {sidebarWidth + 15}px;">
    <slot />
  </div>
</div>

<style>
  .side {
    position: fixed;
    top: 0;
    left: 0;
  }
  .sidebar {
    float: left;
    height: 100%;
    background: #ffcdd2;
    overflow: auto;
  }
  .handle {
    float: left;
    width: 15px;
    height: 100vh;
    background: #0C3E63;
    cursor: ew-resize;
  }
  .content {
    height: 100%;
    overflow: auto;
  }
</style>
