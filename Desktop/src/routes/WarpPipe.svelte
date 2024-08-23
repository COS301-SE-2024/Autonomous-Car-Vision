<script>
    import { Icon, Button } from "svelte-materialify";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { mdiArrowLeft } from "@mdi/js";
    import { onMount } from "svelte";

    import { warp_pipe } from "../stores/store";
    import { push } from "svelte-spa-router";

    onMount(() => {
        console.log($warp_pipe);
    });

    const test = {
        original: 'images/frame_000000.png'
    }

    function back() {
        push("/svelvet");
    }
</script>

<ProtectedRoutes>
    <div class="p-4">
        <div class="w-full flex justify-start">
            <Button class="text-white p-2" icon on:click={back}>
                <Icon path={mdiArrowLeft} size={32}/>
            </Button>
        </div>
        <div class="grid grid-cols-4">
            <div class="grid-cols-1">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                <img src={test.original} alt="Original Image"/>
            </div>
            <div class="grid-cols-1">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                <img src={test.original} alt="Original Image"/>
            </div>
            <div class="grid-cols-1">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                <img src={test.original} alt="Original Image"/>
            </div>
            <div class="grid-cols-1">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                <img src={test.original} alt="Original Image"/>
            </div>
        </div>
        <div class="grid grid-cols-2">
            <div class="grid-cols-1">
                <img src={test.original} alt="Original Image"/>
                
            </div>
            <div class="grid-cols-1">
                <img src={test.original} alt="Original Image"/>
            </div>
        </div>
    </div>
</ProtectedRoutes>
