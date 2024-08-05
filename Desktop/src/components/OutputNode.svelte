<script>
  import {
    Node,
    Anchor,
    generateInput,
    generateOutput,
    Resizer,
  } from "svelvet";

  export let identifier = "";
  export let connectors = [];
  export let position = { x: 0, y: 0 };
  export let label = "Output";
  export let bgColor = "lightblue";

  /**
   * @typedef {Object} InputStructure
   * @property {number} value1
   * @property {number} value2
   * @property {string} option
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
    imageURL: "images/static_processed_output.png",
  };

  // Specify processor function
  /**
   * @param {InputStructure} inputs
   * @returns {number}
   */
  const processor = (inputs) => {
    return inputs.imageURL;
  };
  // Generate a formatted inputs store
  const inputs = generateInput(initialData);
  const output = generateOutput(inputs, processor);

  const key = Object.entries($inputs)[0][0];
</script>

<Node
  let:selected
  minWidth={300}
  minHeigth={300}
  {position}
  id={identifier}
  connections={connectors}
  width={400}
  height={300}
  useDefaults
  {label}
  {bgColor}
>
  <div class="node" class:selected>
    <div class="body">
      <div class="header w-full text-center">
        <h1 class="text-xl font-bold">{label}</h1>
      </div>
      <div class="input-anchors">
        <Anchor dynamic bgColor="green" {key} inputsStore={inputs} input />
      </div>
      <div class="output">
        {#if $output !== "noImage.jpeg"}
          <!-- svelte-ignore a11y-img-redundant-alt -->
          <img src={$output} alt="image.jpeg" />
        {/if}
      </div>
    </div>
  </div>
  <Resizer width height rotation />
</Node>

<style>
  .body {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    align-content: center;
    height: 100%;
  }

  .node {
    width: 100%;
    height: 100%;
    justify-content: center;
  }

  .output {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80%;
    width: 80%;
  }

  .input-anchors {
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 10px;
    top: 40%;
    left: 0px;
  }
</style>
