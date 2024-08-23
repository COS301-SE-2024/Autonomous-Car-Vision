<script>
  import { Node, Anchor, generateInput, generateOutput, Toggle } from "svelvet";

  import { outputPipe } from "../stores/store";

  outputPipe.set([false, false, false, false]);

  export let identifier = "";
  export let connectors = [];
  export let position = { x: 0, y: 0 };
  export let label = "Output";
  export let bgColor = "lightblue";

  let lidarState = false;
  let boundingBoxesState = false;
  let filteredDataState = false;
  let allState = false;
  
  // * @property {string} imageURL
  /**
   * @typedef {Object} InputStructure
   * @property {boolean[]} options
   */

  /**
   * @type {InputStructure}
   */
  let inputStructure = {
    imageURL: "",
    options: [false, false, false, false], // Array to hold the state of the four options
  };

  // Create initial values for your parameters
  /**
   * @type {InputStructure}
   */
  const initialData = {
    // imageURL: "images/static_processed_output.png",
    options: [false, false, false, false], // Default state of toggles
  };

  // Specify processor function
  const processor = (inputs) => {
    return inputs.options;
  };

  // Generate a formatted inputs store
  let inputs = generateInput(initialData);
  const output = generateOutput(inputs, processor);

  const key = Object.entries($inputs)[0][0];

  function toggleLidar() {
    lidarState = !lidarState;
    allState = false;

    outputPipe.set([lidarState,boundingBoxesState,filteredDataState,allState]);
  }

  function toggleBoundingBoxes() {
    boundingBoxesState = !boundingBoxesState;
    allState = false;

    outputPipe.set([lidarState,boundingBoxesState,filteredDataState,allState]);
  }

  function toggleFilteredData() {
    filteredDataState = !filteredDataState;
    allState = false;

    outputPipe.set([lidarState,boundingBoxesState,filteredDataState,allState]);
  }

  function toggleAll() {
    lidarState = false;
    boundingBoxesState = false;
    filteredDataState = false;
    allState = !allState;

    outputPipe.set([lidarState,boundingBoxesState,filteredDataState,allState]);
    console.log($outputPipe);
  }

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
    <div class="body h-full">
      <div class="header w-full text-center">
        <h1 class="text-3xl font-bold">{label}</h1>
      </div>
      <div class="input-anchors">
        <Anchor dynamic bgColor="green" {key} inputsStore={inputs} input />
      </div>
      
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="toggle-switch" on:click={toggleLidar}>
        <input type="checkbox" bind:checked={lidarState} />
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label>Lidar: {lidarState ? 'ON' : 'OFF'}</label>
      </div>

      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="toggle-switch" on:click={toggleBoundingBoxes}>
        <input type="checkbox" bind:checked={boundingBoxesState} />
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label>Bounding boxes: {boundingBoxesState ? 'ON' : 'OFF'}</label>
      </div>
      
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="toggle-switch" on:click={toggleFilteredData}>
        <input type="checkbox" bind:checked={filteredDataState} />
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label>Filtered data: {filteredDataState ? 'ON' : 'OFF'}</label>
      </div>
      
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div class="toggle-switch" on:click={toggleAll}>
        <input type="checkbox" bind:checked={allState} />
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label>All: {allState ? 'ON' : 'OFF'}</label>
      </div>
    </div>
  </div>
</Node>

<style>
  .toggle-switch {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 75%;
    margin: 0 auto;
  }

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

  /* .output {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80%;
    width: 80%;
  } */

  .input-anchors {
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 10px;
    top: 40%;
    left: 0px;
  }
</style>
