<script>
  import {
    Node,
    Anchor,
    Slider,
    RadioGroup,
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
   * @property {number} value1
   * @property {number} value2
   */

  /**
   * @type {InputStructure}
   */
  let inputStructure = {
    value1: 0,
    value2: 0,
  };

  // Create initial values for your parameters
  /**
   * @type {InputStructure}
   */
  const initialData = {
    value1: 10,
    value2: 30,
  };

  // Generate a formatted inputs store
  const inputs = generateInput(initialData);

  // Specify processor function
  /**
   * @param {InputStructure} inputs
   * @returns {number}
   */
  const processor = (inputs) => {
    if (operation === "add") {
      return inputs.value1 + inputs.value2;
    } else if (operation === "subtract") {
      return inputs.value1 - inputs.value2;
    } else if (operation === "multiply") {
      return inputs.value1 * inputs.value2;
    } else {
      return inputs.value1 / inputs.value2;
    }
  };

  // Generate output store
  const output = generateOutput(inputs, processor);

  console.log(label, " ", connectors);
</script>

<Node
  position={position}
  id={identifier}
  connections={connectors}
  width={400}
  height={200}
  useDefaults
  label={label}
  bgColor={bgColor}
>
  <div class="node">
        <!-- <div class="radio-group">
      <RadioGroup
        options={["add", "subtract", "multiply", "divide"]}
        parameterStore={$inputs.option}
      />
    </div> -->
    <h1 class="font-bold text-center text-xl capitalize">
      {label}
    </h1>
    <div class="sliders">
      <Slider parameterStore={$inputs.value1} />
      <Slider parameterStore={$inputs.value2} />
    </div>
    <div class="input-anchors">
      {#each Object.entries($inputs) as [key, value] (key)}
        <Anchor bgColor="green" {key} inputsStore={inputs} input />
      {/each}
    </div>
    <div class="output-anchors">
      <Anchor
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
</Node>

<style>
  .node {
    width: fit-content;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .sliders {
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 20px;
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
