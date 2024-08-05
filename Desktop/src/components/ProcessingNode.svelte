<script>
  import {
    Node,
    Anchor,
    Slider,
    Edge,
    generateInput,
    generateOutput,
  } from "svelvet";

  export let identifier = "";
  export let connectors = [];
  export let position = { x: 0, y: 0 };
  export let operation = "";
  export let label = "Node";
  export let bgColor = "";

  console.log(identifier, ": OPERATION: ", operation);

  /**
   * @typedef {Object} InputStructure
   * @property {number} imageURL
   */

  /**
   * @type {InputStructure}
   */
  let inputStructure = {
    imageURL: "",
  };

  // Create initial values for your parameters
  /**
   * @type {InputStructure}
   */
  const initialData = {
    imageURL: "noImage.jpeg",
  };

  // Generate a formatted inputs store
  let inputs = generateInput(initialData);

  // Specify processor function
  /**
   * @param {InputStructure} inputs
   * @returns {number}
   */
  const processor = (inputs) => {
    return inputs.imageURL;
  };

  // Generate output store
  let output = generateOutput(inputs, processor);

  console.log(label, " ", connectors);
  console.log(initialData)
  console.log(inputs)

  $: inputs => {
    inputs = generateInput(initialData);
    output = generateOutput(inputs, processor);
  }
</script>

<Node
  {position}
  id={identifier}
  connections={connectors}
  width={400}
  height={400}
  useDefaults
  {label}
  {bgColor}
>
  <div class="node">
    <div class="body">
      <h1 class="font-bold text-center text-xl capitalize">
        {label}
      </h1>
      <div class="w-full h-full flex items-center flex-col">
        <h1 class="text-base">
          {$output}
        </h1>
        <div class="showImage">
          {#if $output !== "noImage.jpeg"}
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <img src={$output} alt="image.jpeg" />
          {/if}
        </div>
      </div>
      <div class="input-anchors">
        {#each Object.entries($inputs) as [key, value] (key)}
          <Anchor bgColor="green" {key} inputsStore={inputs} input />
        {/each}
      </div>
      <div class="output-anchors">
        <Anchor
          dynamic
          direction="east"
          id={identifier}
          bgColor="red"
          outputStore={output}
          output
        >
          <Edge slot="edge" color="yellow" label={$output} />
        </Anchor>
      </div>
    </div>
  </div>
</Node>

<style>
  .node {
    width: fit-content;
    display: flex;
    flex-direction: column;
    margin: 10px;
    gap: 20px;
    color: black;
  }

  .body {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    align-content: center;
    height: 100%;
  }

  .showImage {
    width: 20rem;
    height: 20rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .input-anchors {
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 10px;
    top: 40%;
    left: 0px;
  }

  .output-anchors {
    position: absolute;
    right: 0px;
    bottom: 50%;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
</style>
