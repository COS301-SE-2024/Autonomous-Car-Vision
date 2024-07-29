<script>
    import { Node, Anchor, Slider, RadioGroup } from "svelvet";
    import { generateInput, generateOutput } from "svelvet";
    
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
      value1: 10,
      value2: 30,
      option: "multiply",
    };
  
    // Generate a formatted inputs store
    const inputs = generateInput(initialData);
  
    // Specify processor function
    /**
     * @param {InputStructure} inputs
     * @returns {number}
     */
    const processor = (inputs) => {
      if (inputs.option === "add") {
        return inputs.value1 + inputs.value2;
      } else if (inputs.option === "subtract") {
        return inputs.value1 - inputs.value2;
      } else if (inputs.option === "multiply") {
        return inputs.value1 * inputs.value2;
      } else {
        return inputs.value1 / inputs.value2;
      }
    };
  
    // Generate output store
    const output = generateOutput(inputs, processor);
  </script>
  
  <Node width={400} height={200} useDefaults>
    <div class="node">
      <div class="radio-group">
        <RadioGroup
          options={["subtract", "add", "multiply", "divide"]}
          parameterStore={$inputs.option}
        />
      </div>
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
        <Anchor bgColor="red" outputStore={output} output />
      </div>
    </div>
  </Node>
  