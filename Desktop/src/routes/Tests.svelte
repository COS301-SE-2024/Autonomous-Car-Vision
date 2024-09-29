<script>
    import ProtectedRoutes from './ProtectedRoutes.svelte';
    import {Icon, Button} from "svelte-materialify";
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { createEventDispatcher } from 'svelte';
    import {theme} from '../stores/themeStore';

    let uptime= "";
    let loading = true;
    let runTest = "   ..  ";
    const dispatch = createEventDispatcher();
    function Test1() {
        runTest = "Test 1";
        console.log("Test 1");
        loading = false;
    }

    function Test2() {
        runTest = "Test 2";
        console.log("Test 2");
        loading = false;
    }
</script>

<ProtectedRoutes>
    {#if $isLoading}
        <div class="flex justify-center w-full">
        <Spinner />
        </div>
    {:else}
    {#if $theme === 'highVizLight'}
    <div class="user-list text-black-lightText">
        <div class="headerLight text-xl items-center text-center">
            <h2>Tests for Privacy and Security</h2>
            <p>The server has been running for: [time here]{uptime}</p>
        </div>
        <div class="bg-highVizLight grid grid-cols-1  h-full w-full gap-3 py-2 ">
            <Button on:click={() => Test1()}>Perfomance</Button>
            <Button on:click={() => Test2()}>Security</Button>
          </div>
        <div class="text-primary border-2 border-highVizLight-accent rounded-lg h-96 flex items-center justify-center col-span-1 row-span-2">
           
                {#if loading}
                    <div class="flex justify-center w-full">
                        <Spinner />
                    </div>
                {:else}
                    <p>Results for {runTest} ready!</p>
                {/if}
        </div>
    </div>
    {:else}
    <div class="user-list text-theme-dark-lightText">
        <div class="header text-xl items-center text-center">
            <h2>Tests for Privacy and Security</h2>
            <p>The server has been running for:  [time here] {uptime}</p>
        </div>
        <div class="bg-highVizDark grid grid-cols-1 h-full w-full gap-3 py-2 text-white">
            <Button on:click={ () => Test1()}>Perfomance</Button>
            <Button on:click={ () => Test2()}>Security</Button>
        </div>
        <div class="text-theme-dark  border-highVizDark-primary border-2 h-96 rounded-lg flex items-center justify-center col-span-1 row-span-2">
            {#if loading}
                <div class="flex justify-center w-full">
                    <Spinner />
                </div>
            {:else}
                <p>Results {runTest} ready!</p>
            {/if}
       </div>
    </div>
    {/if}
    {/if}
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

    .headerLight {
        color: rgb(0, 0, 0);
        padding: 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        /* margin-left: 10px; */
    }
</style>
