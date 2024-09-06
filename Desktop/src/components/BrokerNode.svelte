<script>
    import { onMount } from "svelte";
    import { Node, Edge, Anchor } from "svelvet";
    import { TeamAgents, TeamClients } from "../stores/store";
    import { get } from "svelte/store";

    export let dimensions;
    export let nodeData;

    let nodeType = nodeData.type;

    let agents = get(TeamAgents);
    let clients = get(TeamClients);
    let edgeColor = "gray";

    let bgColor = "gray";
    const getRanHex = (size = 6) => {
        const hexRef = "0123456789abcdef";
        let hexColor = "";

        // Function to calculate brightness
        const calculateBrightness = (hex) => {
            let r = parseInt(hex.substring(0, 2), 16);
            let g = parseInt(hex.substring(2, 4), 16);
            let b = parseInt(hex.substring(4, 6), 16);
            return (r * 299 + g * 587 + b * 114) / 1000;
        };

        // Generate a hex color and ensure it's not too light
        while (true) {
            hexColor = "";
            for (let n = 0; n < size; n++) {
                hexColor += hexRef[Math.floor(Math.random() * 16)];
            }

            // Check if the color is too bright
            let brightness = calculateBrightness(hexColor);
            if (brightness < 200) {
                // Adjust the threshold as needed
                break;
            }
        }

        return hexColor;
    };

    function setBGColour() {
        if (nodeType === "Broker") {
            bgColor = `blue`;
        }
    }

    function showConnectionToAgent() {
        console.log(nodeData);
        console.log(nodeType);

        // Reset all edge colors
        resetEdgeColors();

        // Access the writable stores to update agents/clients
        let agentBooleans = get(TeamAgents);
        let clientBooleans = get(TeamClients);

        agentBooleans.fill(false);
        clientBooleans.fill(false);

        // If the node has clients, mark them as selected
        if (nodeData?.agents) {
            agentBooleans = agentBooleans.map((value, index) => {
                return true;
            });
        }

        // Update the writable stores
        TeamAgents.set(agentBooleans);
        TeamClients.set(clientBooleans);

        console.log("Updated TeamAgents:", agentBooleans);
        console.log("Updated TeamClients:", clientBooleans);
    }

    function resetEdgeColors() {
        edgeColor = "gray";
    }

    function updateEdgeColor() {
        // Check if the node is a Broker
        if (nodeType === "Broker") {
            // Check if any agent is active
            const anyAgentActive = agents.some((agent) => agent);

            // Set edge color based on the presence of active agents
            if (anyAgentActive) {
                edgeColor = "blue";
            } else {
                edgeColor = "gray"; // Default color if no active agents
            }
        } else {
            edgeColor = "gray"; // Default color if node is not a Broker
        }
    }

    onMount(() => {
        updateEdgeColor();
        setBGColour();
    });

    TeamAgents.subscribe((newAgents) => {
        agents = newAgents;
        resetEdgeColors();
        updateEdgeColor(); // Re-run to reflect the latest store values
    });

    TeamClients.subscribe((newClients) => {
        clients = newClients;
        resetEdgeColors();
        updateEdgeColor(); // Re-run to reflect the latest store values
    });
</script>

<Node
    useDefaults
    id={nodeData.id}
    position={nodeData.position}
    width={dimensions.width}
    height={dimensions.height}
    editable={false}
    {bgColor}
    on:nodeClicked={showConnectionToAgent}
>
    <div class="w-full flex flex-col justify-center h-full">
        <div class="fixed h-full w-full flex justify-center items-center">
            {#each nodeData.anchors as anchor}
                {#if anchor.type === "input"}
                    <Anchor
                        invisible
                        direction="north"
                        locked
                        input
                        id={anchor.id}
                        connections={[anchor.id]}
                    />
                {/if}
            {/each}
        </div>
        <h1 class="text-3xl text-center">
            {nodeData.label}
        </h1>
    </div>
</Node>

<style>
    :global(.output.connected) {
        background-color: red !important;
    }

    :global(.input.connected) {
        background-color: rgb(95, 218, 255) !important;
    }
</style>
