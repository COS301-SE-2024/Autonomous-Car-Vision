<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { Svelvet, Node, Anchor } from "svelvet";
    import TeamNode from "../components/TeamNode.svelte";

    // Define the initial nodes with anchors
    let nodes = [
        {
            id: "4",
            type: "Manager",
            position: { x: 500, y: -400 },
            label: "Manager",
            anchors: [
                { id: "out6", type: "output", out: "1" },
                { id: "out5", type: "output", out: "2" },
                { id: "out4", type: "output", out: "3" },
            ],
        },
        {
            id: "1",
            type: "Manager/Supervisor",
            position: { x: 100, y: 100 },
            label: "Supervisor",
            anchors: [
                { id: "in1", type: "input" },
                { id: "out1", type: "output", out: "2" }, // output anchor for connections
            ],
        },
        {
            id: "2",
            type: "Supervisor",
            position: { x: 500, y: 300 },
            label: "Supervisor",
            anchors: [
                { id: "in2", type: "input" }, // Input anchor for connections
                { id: "out2", type: "output", out: "3" }, // Output anchor for connections
            ],
        },
        {
            id: "3",
            type: "Client",
            position: { x: 900, y: 500 },
            label: "Client",
            anchors: [
                { id: "in3", type: "input" }, // Input anchor for connections
            ],
        },
    ];

    function makeNodes(JsonPayload) {
        // HIERARCHY
        // BROKER
        // Connected AGENTS
    }
</script>

<ProtectedRoutes>
    <Svelvet TD fitView theme="dark" edgeStyle="bezier">
        {#each nodes as node}
            <TeamNode id={node.id} position={node.position} dimensions={ {width: 150, height: 100} } nodeData={node} />
        {/each}
    </Svelvet>
</ProtectedRoutes>

<style>
</style>
