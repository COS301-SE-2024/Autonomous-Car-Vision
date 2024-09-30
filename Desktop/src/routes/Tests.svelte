<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { Icon, Button } from "svelte-materialify";
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { createEventDispatcher } from "svelte";
    import { theme } from "../stores/themeStore";
    import { onMount } from "svelte";

    let uptime = "";
    let loading = true;
    let runTest = "   ..  ";
    const dispatch = createEventDispatcher();
    let testResults = {};

    let HOST_IP = "";

    let performanceTestStarted = false;

    onMount(async () => {
        HOST_IP = await window.electronAPI.getHostIp();

        // Request uptime
        uptime = await window.electronAPI.requestUptime();
        uptime = uptime.uptime;

        // Fetch test data
        loading = false;
    });
    
    const PerformanceTest = async () => {
        performanceTestStarted = true;
        runTest = "Performance Test";    
        testResults = await window.electronAPI.getTestData();
        performanceTestStarted = false;
    };

    function SecurityTest() {
        runTest = "Test 2";
        loading = false;
    }
</script>

<ProtectedRoutes>
    {#if loading}
        <div class="flex justify-center w-full h-fit">
            <Spinner />
        </div>
    {:else if $theme === "highVizLight"}
        <div class="user-list text-black-lightText">
            <div class="headerLight text-xl items-center text-center">
                <h2>Tests for Privacy and Security</h2>
                <p>The server has been running for: {uptime}%</p>
            </div>
            <div class="bg-highVizLight grid grid-cols-1 gap-3 py-2">
                <Button on:click={PerformanceTest}>Start Perfomance Tests</Button>
            </div>
            <div class="results-container">
                {#if performanceTestStarted}
                    <div class="flex justify-center w-full">
                        <Spinner />
                    </div>
                {:else}
                    <div class="py-4">
                        <h1 class="text-4xl font-bold text-center">Performance Test</h1>
                        <div class="flex flex-row justify-between text-2xl font-bold">
                            <h1>Number of Tests</h1>
                            <h1>{Object.keys(testResults.data || {}).length}</h1>
                        </div>
                        <table class="table-auto w-full">
                            <thead>
                                <tr>
                                    <th>Endpoints</th>
                                    <th>Result (seconds)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each Object.entries(testResults.data || {}) as [endpoint, result]}
                                    <tr>
                                        <td>{endpoint}</td>
                                        <td>{result.toFixed(5)}</td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {/if}
            </div>
        </div>
    {:else}
        <div class="user-list text-theme-dark-lightText">
            <div class="header text-xl items-center text-center">
                <h2>Tests for Privacy and Security</h2>
                <p>The server has been running for: {uptime}</p>
            </div>
            <div class="bg-highVizDark grid grid-cols-1 gap-3 py-2 text-white">
                <Button on:click={PerformanceTest}>Perfomance</Button>
                <!-- <Button on:click={SecurityTest}>Security</Button> -->
            </div>
            <div class="results-container">
                {#if performanceTestStarted}
                    <div class="flex justify-center w-full h-fit">
                        <Spinner />
                    </div>
                {:else}
                <div class="py-4">
                    <h1 class="text-4xl font-bold text-center">Performance Test</h1>
                    <div class="flex flex-row justify-between text-2xl font-bold">
                        <h1>Number of Tests</h1>
                        <h1>{Object.keys(testResults.data || {}).length}</h1>
                    </div>
                    <table class="table-auto w-full">
                        <thead>
                            <tr>
                                <th>Endpoints</th>
                                <th>Result (seconds)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each Object.entries(testResults.data || {}) as [endpoint, result]}
                                <tr>
                                    <td>{endpoint}</td>
                                    <td>{result.toFixed(5)}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
                {/if}
            </div>
        </div>
    {/if}
</ProtectedRoutes>

<style>
    .user-list {
        width: 100%;
        max-width: 750px;
        margin: 0 auto;
    }
    .header,
    .headerLight {
        padding: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
    .results-container {
        border: 2px solid inherit;
        border-radius: 8px;
        padding: 20px;
        overflow-x: auto;
        max-height: 400px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th,
    td {
        padding: 12px;
        border: 1px solid inherit;
        text-align: left;
    }
</style>
