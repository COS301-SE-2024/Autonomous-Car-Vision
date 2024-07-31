<script>
  import { Node, Anchor, Slider, generateInput, generateOutput } from "svelvet";
  import { Connections } from "svelvet";
  import { writable } from "svelte/store";

  export let Identifier = "";
  export let connectors = [];
  export let position = { x: 0, y: 0 };

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
    value1: 0,
    value2: 0,
    option: "default",
  };

  // Create initial values for your parameters
  /**
   * @type {InputStructure}
   */
  const initialData = {
    value1: 0,
    value2: 0,
    option: "default",
  };

  // Specify processor function
  /**
   * @param {InputStructure} inputs
   * @returns {number}
   */
  const processor = (inputs) => {
    return inputs.value1;
  };
  // Generate a formatted inputs store
  const inputs = generateInput(initialData);
  const output = generateOutput(inputs, processor);

  const key = Object.entries($inputs)[0][0];
</script>

<Node
  {position}
  id={Identifier}
  connections={connectors}
  width={400}
  height={200}
  useDefaults
>
  <div class="node">
	<div class="header w-full text-center">
		<h1 class="text-xl font-bold">
			Output
		</h1>
	</div>
    <div class="input-anchors">
        <Anchor bgColor="green" {key} inputsStore={inputs} input />
    </div>
    <div class="output">
      {$output}
    </div>
  </div>
</Node>

<style>
	.node {
		width: 100%;
		height: 100%;
		background-color: #f0f0f0;
		justify-content: center;
	}

	.output {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
		font-size: 32px
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
