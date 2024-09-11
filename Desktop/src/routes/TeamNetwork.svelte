<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { Svelvet } from "svelvet";
    import TeamNode from "../components/TeamNode.svelte";
    import { onMount } from "svelte";
    import { TeamClients, TeamAgents } from "../stores/store";
    import TeamConnectionNodes from "../components/TeamConnectionNodes.svelte";
    import BrokerNode from "../components/BrokerNode.svelte";
    import ManagerNode from "../components/ManagerNode.svelte";

    // Define the initial nodes with anchors
    let nodes = [
        {
            id: "1",
            type: "Broker",
            position: { x: 100, y: -200 },
            label: "Broker",
            anchors: [
                { id: "in1", type: "input" }, // Input for Agents
            ],
            agents: ["10", "11", "12", "13"],
        },
        {
            id: "2",
            type: "Manager",
            position: { x: 575, y: -200 },
            label: "Manager",
            anchors: [
                { id: "out2", type: "output", out: "1" }, // Output to Broker
                { id: "in2", type: "input" }, // Input for Clients
            ],
            clients: ["3", "4", "5", "6"],
            agents: ["10"],
        },
        {
            id: "3",
            type: "Client",
            position: { x: 0, y: 300 },
            label: "Client 0",
            anchors: [
                { id: "out1", type: "output", out: "2" }, // output anchor
            ],
            agents: ["10", "11"],
        },
        {
            id: "4",
            type: "Client",
            position: { x: 350, y: 300 },
            label: "Client 1",
            anchors: [
                { id: "out1", type: "output", out: "2" }, // output anchor
            ],
            agents: ["10", "13"],
        },
        {
            id: "5",
            type: "Client",
            position: { x: 800, y: 300 },
            label: "Client 2",
            anchors: [
                { id: "out1", type: "output", out: "2" }, // output anchor
            ],
            agents: ["11", "12"],
        },
        {
            id: "6",
            type: "Client",
            position: { x: 1150, y: 300 },
            label: "Client 3",
            anchors: [
                { id: "out1", type: "output", out: "2" }, // output anchor
            ],
            agents: ["12", "13"],
        },
        // AGENTS
        {
            id: "10",
            type: "Agent",
            position: { x: -500, y: -500 },
            label: "Agent 0",
            anchors: [{ id: "out1", type: "output", out: "1" }],
            clients: ["3", "4"],
        },
        {
            id: "11",
            type: "Agent",
            position: { x: -150, y: -500 },
            label: "Agent 1",
            anchors: [{ id: "out1", type: "output", out: "1" }],
            clients: ["3", "5"],
        },
        {
            id: "12",
            type: "Agent",
            position: { x: 400, y: -500 },
            label: "Agent 2",
            anchors: [{ id: "out1", type: "output", out: "1" }],
            clients: ["5", "6"],
        },
        {
            id: "13",
            type: "Agent",
            position: { x: 700, y: -500 },
            label: "Agent 3",
            anchors: [{ id: "out1", type: "output", out: "1" }],
            clients: ["4", "6"],
        },
    ];

    onMount(() => {
        let agentBooleans = [];
        let clientBooleans = [];

        nodes.forEach((node) => {
            if (node.type === "Agent") {
                agentBooleans.push(false);
            } else if (node.type === "Client") {
                clientBooleans.push(false);
            }
        });

        // Update the writable stores
        TeamAgents.set(agentBooleans);
        TeamClients.set(clientBooleans);
    });

    let testPayload = {
        clients: [
            {
                id: 1,
                name: "John Doe",
                agents: [1, 2],
            },
            {
                id: 2,
                name: "Dave Marshall",
                agents: [2],
            },
        ],
        agents: [
            {
                id: 1,
            },
            {
                id: 2,
            },
            {
                id: 3,
            },
        ],
    };

    // Edge cases
    // Everyone has similar priviledges, so no Manager then everyone connects to the Broker

    function makeNodes(JsonPayload) {
        let NodesMake = [];

        // Step 1: Create the Broker node
        let brokerNode = {
            id: "1",
            type: "Broker",
            position: { x: 100, y: -200 },
            label: "Broker",
            anchors: [
                { id: "in1", type: "input" }, // Input for Agents
            ],
            agents: JsonPayload.agents.map((agent) => agent.id.toString()),
        };
        NodesMake.push(brokerNode);

        // Step 2: Create Agent nodes and connect them to the Broker
        JsonPayload.agents.forEach((agent, index) => {
            let agentNode = {
                id: agent.id.toString(),
                type: "Agent",
                position: { x: index * 200 - 500, y: -500 }, // Adjust positions dynamically
                label: `Agent ${index}`,
                anchors: [
                    { id: "out1", type: "output", out: "1" }, // Connected to Broker
                ],
                clients: [], // Will populate later with connected clients
            };
            NodesMake.push(agentNode);
        });

        // Step 3: Create Client nodes and connect them to their respective Agents
        JsonPayload.clients.forEach((client, clientIndex) => {
            let clientNode = {
                id: (client.id + 2).toString(), // Client IDs start from 2+ since 1 is for Broker
                type: "Client",
                position: { x: clientIndex * 300, y: 300 }, // Adjust positions dynamically
                label: `Client ${clientIndex}`,
                anchors: [
                    {
                        id: "out1",
                        type: "output",
                        out: client.agents[0].toString(),
                    }, // Output connected to an agent
                ],
                agents: client.agents.map((agentId) => agentId.toString()),
            };

            // Add the client to the connected agents' clients list
            client.agents.forEach((agentId) => {
                let agentNode = NodesMake.find(
                    (node) =>
                        node.id === agentId.toString() && node.type === "Agent",
                );
                if (agentNode) {
                    agentNode.clients.push(clientNode.id);
                }
            });

            NodesMake.push(clientNode);
        });

        return NodesMake;
    }

    console.log(makeNodes(testPayload));
</script>

<ProtectedRoutes>
    <Svelvet TD fitView theme="dark" edgeStyle="bezier">
        {#each nodes as node}
            {#if node.type == "Agent"}
                <TeamConnectionNodes
                    id={node.id}
                    position={node.position}
                    dimensions={{ width: 150, height: 100 }}
                    nodeData={node}
                />
            {:else if node.type == "Broker"}
                <BrokerNode
                    id={node.id}
                    position={node.position}
                    dimensions={{ width: 150, height: 100 }}
                    nodeData={node}
                />
            {:else if node.type == "Manager"}
                <ManagerNode
                    id={node.id}
                    position={node.position}
                    dimensions={{ width: 150, height: 100 }}
                    nodeData={node}
                />
            {:else}
                <TeamNode
                    id={node.id}
                    position={node.position}
                    dimensions={{ width: 150, height: 100 }}
                    nodeData={node}
                />
            {/if}
        {/each}
    </Svelvet>
</ProtectedRoutes>

<style>
</style>
