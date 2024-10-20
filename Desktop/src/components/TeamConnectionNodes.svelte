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

        const calculateBrightness = (hex) => {
            let r = parseInt(hex.substring(0, 2), 16);
            let g = parseInt(hex.substring(2, 4), 16);
            let b = parseInt(hex.substring(4, 6), 16);
            return (r * 299 + g * 587 + b * 114) / 1000;
        };

        while (true) {
            hexColor = "";
            for (let n = 0; n < size; n++) {
                hexColor += hexRef[Math.floor(Math.random() * 16)];
            }

            let brightness = calculateBrightness(hexColor);
            if (brightness < 200) {
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
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                obj[key] = false;
            }
        }
    }

    function showConnectionToClient() {
        resetEdgeColors();

        let agentBooleans = get(TeamAgents);
        let clientBooleans = get(TeamClients);

        resetBooleanMaps(agentBooleans);
        resetBooleanMaps(clientBooleans);

        if (nodeData?.clients) {
            nodeData.clients.forEach((clientID) => {
                if (clientBooleans.hasOwnProperty(clientID)) {
                    clientBooleans[clientID] = true;
                }
            });
        }

        if (nodeType === "Agent") {
            agentBooleans[nodeData.booleanID.id] = true;
        }
        
        TeamAgents.set(agentBooleans);
        TeamClients.set(clientBooleans);
    }

    function resetEdgeColors() {
        edgeColor = "gray";
    }

    function updateEdgeColor() {
        if (nodeType === "Agent" && agents[nodeData.booleanID.id]) {
            edgeColor = "blue";
        } else if (
            nodeType === "Client" &&
            clients[nodeData.booleanID.id]
        ) {
            edgeColor = "green";
        } else {
            edgeColor = "gray";
        }
    }

    onMount(() => {
        setBGColour();
        updateEdgeColor();
    });

    TeamAgents.subscribe((newAgents) => {
        agents = newAgents;
        resetEdgeColors();
        updateEdgeColor();
    });

    TeamClients.subscribe((newClients) => {
        clients = newClients;
        resetEdgeColors();
        updateEdgeColor();
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
    on:nodeClicked={showConnectionToClient}
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
        <h1 class="text-3xl text-center text-white">
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
                        <Edge
                            slot="edge"
                            end="arrow"
                            straight
                            animate
                            color={edgeColor}
                        />
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
