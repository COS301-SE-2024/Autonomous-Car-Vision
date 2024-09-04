<script>
    import { onMount } from "svelte";
    import { Node, Edge, Anchor, generateInput } from "svelvet";

    export let dimensions;
    export let nodeData;

    let nodeType = nodeData.type;

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

    console.log(getRanHex(6));

    function setBGColour() {
        if (nodeType === "Manager") {
            bgColor = `red`;
        } else if (nodeType === "Manager/Supervisor") {
            bgColor = `#${getRanHex(6)}`;
        } else if (nodeType === "Supervisor") {
            bgColor = `#${getRanHex(6)}`;
        } else {
            bgColor = `#${getRanHex(6)}`;
        }
    }

    onMount(() => {
        setBGColour();
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
                        <!-- {#if nodeType == "Supervisor"}
                                <Edge slot="edge" color="yellow" />
                            {:else if nodeType == "Manager"}
                                <Edge slot="edge" color="red" />
                            {:else if nodeType == "Manager/Supervisor"} -->
                        <Edge slot="edge" color="white" />
                        <!-- {:else}
                                <Edge slot="edge" color="green" />
                            {/if} -->
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
