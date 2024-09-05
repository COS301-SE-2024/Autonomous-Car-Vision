<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { Svelvet, Node, Anchor } from "svelvet";
    import TeamNode from "../components/TeamNode.svelte";

    // Define the initial nodes with anchors
    let nodes = [
        {
            id: "1",
            type: "Broker",
            position: { x: 100, y: -200 },
            label: "Broker",
            anchors: [
                { id: "in1", type: "input" },
                { id: "out1", type: "output", out: "2" },
            ],
        },
        {
            id: "2",
            type: "Manager",
            position: { x: 100, y: 200 },
            label: "Manager",
            anchors: [
                { id: "in1", type: "input" }, // Input from Broker
                { id: "out2", type: "output", out: "3" }, // Client 0
                { id: "out3", type: "output", out: "4" }, // Client 1
                { id: "out4", type: "output", out: "5" }, // Client 2
                { id: "out5", type: "output", out: "6" }, // Client 3
            ],
        },
        {
            id: "3",
            type: "Client 0",
            position: { x: -500, y: 500 },
            label: "Client 0",
            anchors: [
                { id: "in2", type: "input" }, // Input anchor from broker
            ],
        },
        {
            id: "4",
            type: "Client",
            position: { x: -150, y: 500 },
            label: "Client 1",
            anchors: [
                { id: "in3", type: "input" }, // Input anchor for connections
            ],
        },
        {
            id: "5",
            type: "Client",
            position: { x: 400, y: 500 },
            label: "Client 2",
            anchors: [
                { id: "in3", type: "input" }, // Input anchor for connections
            ],
        },
        {
            id: "6",
            type: "Client",
            position: { x: 700, y: 500 },
            label: "Client 3",
            anchors: [
                { id: "in3", type: "input" }, // Input anchor for connections
            ],
        },
        // AGENTS
        {
            id: "10",
            type: "Agent",
            position: { x: -500, y: -500 },
            label: "Agent 1",
            anchors: [
                { id: "out1", type: "output", out: "1"},
            ],
        },
        {
            id: "11",
            type: "Agent",
            position: { x: -150, y: -500 },
            label: "Agent 2",
            anchors: [
                { id: "out1", type: "output", out: "1"},
            ],
        },
        {
            id: "12",
            type: "Agent",
            position: { x: 400, y: -500 },
            label: "Agent 3",
            anchors: [
                { id: "out1", type: "output", out: "1"},
            ],
        },
        {
            id: "13",
            type: "Agent",
            position: { x: 700, y: -500 },
            label: "Agent 4",
            anchors: [
                { id: "out1", type: "output", out: "1"},
            ],
        },
    ];

    function makeNodes(JsonPayload) {
        // HIERARCHY
        // BROKER
        // Connected AGENTS

        // Broker
        //  Agents
        //      Store
        //      Process
        
        // Grouped

        // Manager
        // Connected Clients

        
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
