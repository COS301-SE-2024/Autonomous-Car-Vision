<!--src/routes/ProtectedRoute.svelte-->
<script>
  import { token } from "../stores/auth";
  import { onMount } from "svelte";
  import { navigate } from "@sveltejs/kit/navigation"; 
  import SidebarV2 from "../components/SidebarV2.svelte";
  import { sidebarWidth } from "../stores/store";
  import { theme } from '../stores/themeStore';


  let currentTheme;

  theme.subscribe(value => {
    currentTheme = value;
    document.documentElement.className = currentTheme; 
  });

  let authToken;

  $: token.subscribe((value) => {
    authToken = window.electronAPI.getToken();
  });

  onMount(() => {
    if (!authToken) {
      navigate("#login"); 
    }
  });

  const minOffset = 75;
  const maxOffset = 250;

  function handleMouseMove(event) {
    let offset = event.pageX;

    offset = offset < minOffset ? minOffset : offset;
    offset = offset > maxOffset ? maxOffset : offset;

    if (offset < 150) {
      sidebarWidth.set(75);
    } else {
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
    sidebarWidth.set(220);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  });
</script>

 {#if $theme === 'highVizLight'}
  <div
  class="h-screen w-full overflow-none overscroll-none bg-dark-background_secondary"
>
  <div class="side">
    <div class="sidebar" style="width: {$sidebarWidth}px;">
      <SidebarV2 width={$sidebarWidth} />
    </div>
    <div class="handle" on:mousedown={handleMouseDown} role="button" tabindex="0">
      <div class="handle-inner"></div>
    </div>
  </div>
  <div class="pr-2 pt-2 pb-2 h-screen">
    <div class="main-contentLight" style="margin-left: {$sidebarWidth + 10}px;">
      <slot />
    </div>
  </div>
</div>
{:else}
  <div
  class="h-screen w-full overflow-none overscroll-none bg-dark-background_secondary"
  >
  <div class="side">
    <div class="sidebar" style="width: {$sidebarWidth}px;">
      <SidebarV2 width={$sidebarWidth} />
    </div>
    <div class="handle" on:mousedown={handleMouseDown} role="button" tabindex="0">
      <div class="handle-inner"></div>
    </div>
  </div>
  <div class="pr-2 pt-2 pb-2 h-screen">
    <div class="main-content" style="margin-left: {$sidebarWidth + 10}px;">
      <slot />
    </div>
  </div>
  </div>
{/if}


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
  
  .main-content {
    height: 100%;
    overflow: auto;
    background-image: linear-gradient(180deg, #001524, #181818);
    border-radius: 15px;
  }

   .main-contentLight {
    height: 100%;
    overflow: auto;
    background-image: linear-gradient(180deg, #F8F8F8, #B6D9E8);
    border-radius: 15px;
  }
  .main-contentLight::-webkit-scrollbar {
    display: none;
  }
  .main-content::-webkit-scrollbar {
    display: none;
  }
</style>
