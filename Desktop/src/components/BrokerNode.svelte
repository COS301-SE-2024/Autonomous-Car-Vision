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
        if (nodeType === "Broker") {
            bgColor = `blue`;
        }
    }

    function resetBooleanMaps(obj) {
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                obj[key] = false;
            }
        }
    }

    function showConnectionToAgent() {
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

        TeamAgents.set(agentBooleans);
        TeamClients.set(clientBooleans);
    }

    function resetEdgeColors() {
        edgeColor = "gray";
    }

    function updateEdgeColor() {
        if (nodeType === "Agent" && agents[nodeData.booleanID.id]) {
            edgeColor = "blue";
        } else if (nodeType === "Client" && clients[nodeData.booleanID.id]) {
            edgeColor = "green";
        } else {
            edgeColor = "gray";
        }
    }

    onMount(() => {
        updateEdgeColor();
        setBGColour();
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
        <div class="text-white">
            <h1 class="text-3xl text-center uppercase">
                {nodeData.team_name}
            </h1>
            <h1 class="text-3xl text-center">
                {nodeData.label}
            </h1>
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
