<!--src/routes/ProtectedRoute.svelte-->
<script>
  import { token } from "../stores/auth";
  import { onMount } from "svelte";
  import { navigate } from "@sveltejs/kit/navigation"; // If using SvelteKit for navigation
  import Sidebar from "../components/Sidebar.svelte";
  import SidebarV2 from "../components/SidebarV2.svelte";
  import { sidebarWidth } from "../stores/store";

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

  const minOffset = 75;
  const maxOffset = 250;

  function handleMouseMove(event) {
    let offset = event.pageX;

    offset = offset < minOffset ? minOffset : offset;
    offset = offset > maxOffset ? maxOffset : offset;

    if (offset < 150) {
      // sidebarWidth = 75;
      sidebarWidth.set(75);
    } else {
      // sidebarWidth = offset;
      sidebarWidth.set(offset);
    }
  }

  function handleMouseUp() {
    document.querySelector('.handle-inner').classList.remove('highlighted');
    window.removeEventListener("mousemove", handleMouseMove);
    window.removeEventListener("mouseup", handleMouseUp);
  }

  function handleMouseDown() {
    document.querySelector('.handle-inner').classList.add('highlighted');
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
  }

  onMount(() => {
    // Cleanup event listeners if the component is unmounted
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  });
</script>

<!-- Slot to render the protected content if authenticated -->
<div
  class="h-screen w-full overflow-none overscroll-none bg-dark-background_secondary"
>
  <div class="side">
    <div class="sidebar" style="width: {$sidebarWidth}px;">
      <SidebarV2 width={$sidebarWidth} />
    </div>
    <div class="handle" on:mousedown={handleMouseDown}>
      <div class="handle-inner"></div>
    </div>
  </div>
  <div class="pr-2 pt-2 pb-2 h-screen">
    <div class="main-content" style="margin-left: {$sidebarWidth + 10}px;">
      <slot />
    </div>
  </div>
</div>

<style>
  .side {
    position: relative;
    top: 0;
    left: 0;
  }
  
  .sidebar {
    float: left;
    height: 100vh;
    background: none;
    overflow: hidden;
    padding: 10px 0 10px 10px;
  }
  
  .handle {
    float: left;
    width: 10px;
    height: 100vh;
    cursor: grab;
    display: grid;
    place-items: center;
  }

  .handle-inner {
    height: 95%;
    padding-right: 1px;
    padding-left: 1px;
    border-radius: 15px;
  }

  .handle:hover  .handle-inner {
    background-color: #fff;
  }

  .handle-inner.highlighted {
    background-color: #fff;
  }
  
  .main-content {
    height: 100%;
    overflow: auto;
    background-image: linear-gradient(180deg, #001524, #181818);
    border-radius: 15px;
  }
  
  .main-content::-webkit-scrollbar {
    display: none;
  }
</style>
