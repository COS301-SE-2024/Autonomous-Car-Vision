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
        if (nodeType === "Manager") {
            bgColor = `red`;
        } else if (nodeType === "Broker") {
            bgColor = `blue`;
        } else if (nodeType === "Agent") {
            bgColor = `#${getRanHex(6)}`;
        } else {
            bgColor = `#${getRanHex(6)}`;
        }
    }

    function resetBooleanMaps(obj) {
        Object.keys(obj).forEach((key) => {
            obj[key] = false;
        });
    }

    function showConnectionToAgent() {
        console.log(nodeData.booleanID);
        console.log(nodeType);

        // Reset all edge colors
        resetEdgeColors();

        // Access the writable stores to update agents/clients
        let agentBooleans = get(TeamAgents);
        let clientBooleans = get(TeamClients);

        // Reset boolean arrays
        resetBooleanMaps(agentBooleans);
        resetBooleanMaps(clientBooleans);

        // If the node has clients, mark them as selected
        if (nodeData?.clients) {
            nodeData.clients.forEach((cleintId) => {
                // Ensure we're updating the boolean based on the correct key
                if (clientBooleans.hasOwnProperty(cleintId)) {
                    clientBooleans[cleintId] = true; // Set to true for active agents
                }
            });
        }

        // Update agent booleans
        if (nodeType === "Agent") {
            agentBooleans[Number(nodeData.booleanID)] = true;
        } else if (nodeType === "Broker") {
            edgeColor = "blue";
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
        // Update color based on agents or clients
        if (nodeType === "Agent" && agents[Number(nodeData.booleanID)]) {
            edgeColor = "blue"; // Example: change to blue if agent is active
        } else if (
            nodeType === "Client" &&
            clients[Number(nodeData.booleanID)]
        ) {
            edgeColor = "green"; // Example: change to green if client is active
        } else {
            edgeColor = "gray"; // Default color
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
    <div class="flex flex-col justify-between h-full">
        <div class="flex flex-row justify-center">
            {#each nodeData.anchors as anchor}
                {#if anchor.type === "input"}
                    <Anchor
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
        <div class="flex flex-row justify-center">
            {#each nodeData.anchors as anchor}
                {#if anchor.type === "output"}
                    <Anchor
                        direction="south"
                        locked
                        output
                        id={anchor.id}
                        connections={[anchor.id, anchor.out]}
                    >
                        <Edge slot="edge" end="arrow" color={edgeColor} />
                    </Anchor>
                {/if}
            {/each}
        </div>
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
