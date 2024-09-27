<script>
    import { onMount } from "svelte";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { writable } from "svelte/store";

    import { Svelvet, Node } from "svelvet";

    const team_Structure = [
        {
            id: 1,
            name: "John Doe",
            type: "Client",
        },
        {
            id: 2,
            name: "Tester",
            type: "Agent",
        },
    ];

    const nodes = writable([]);
    const edges = writable([]);
    let nodeIdCounter = 0;

    onMount({});
</script>

<ProtectedRoutes>
    <div class="team"></div>
    <Svelvet theme="dark">
        <Node />
        <Node bgColor="red" label="Node" />
    </Svelvet>
</ProtectedRoutes>
