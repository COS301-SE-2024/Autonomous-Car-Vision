<script>
  import { Node, Anchor, generateInput, generateOutput, Toggle } from "svelvet";
  import { Switch } from "svelte-materialify";
  import { outputPipe } from "../stores/store";
  import { onMount } from "svelte";

  onMount(() => {
    outputPipe.set([false, false, false, false]);
  });

  export let identifier = "";
  export let connectors = [];
  export let position = { x: 0, y: 0 };
  export let label = "Output";
  export let bgColor = "lightblue";

  // * @property {string} imageURL
  /**
   * @typedef {Object} InputStructure
   * @property {boolean[]} options
   */

  /**
   * @type {InputStructure}
   */
  let inputStructure = {
    null: "",
  };

  // Create initial values for your parameters
  /**
   * @type {InputStructure}
   */
  const initialData = {
    null: ""
  };

  // Generate a formatted inputs store
  let inputs = generateInput(initialData);

  const key = Object.entries($inputs)[0][0];

  outputPipe.subscribe(() => {
    if ($outputPipe[0] && $outputPipe[1] && $outputPipe[2]) {
      outputPipe.set([false, false, false, true]);    }
    if (
      ($outputPipe[0] || $outputPipe[1] || $outputPipe[2]) &&
      $outputPipe[3]
    ) {
      $outputPipe[3] = false;
    }
    console.log($outputPipe);
  });
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
  editable={false}
>
  <div class="node" class:selected>
    <div class="body h-full">
      <div class="header w-full text-center">
        <h1 class="text-3xl font-bold">{label}</h1>
      </div>
      <div class="input-anchors">
        <Anchor dynamic bgColor="green" {key} input />
      </div>
      <div class="switches justify-center">
        <Switch bind:checked={$outputPipe[0]} value={false}></Switch>
        <p class="text-xl">
          Lidar
        </p>
      </div>
      <div class="switches justify-center">
        <Switch bind:checked={$outputPipe[1]} value={false}
          ></Switch
        >
        <p class="text-xl">
          Bounding Boxes
        </p>
      </div>
      <div class="switches justify-center">
        <Switch bind:checked={$outputPipe[2]} value={false}
          ></Switch
        >
        <p class="text-xl">
          Filtered Data
        </p>
      </div>
      <div class="switches justify-center">
        <Switch bind:checked={$outputPipe[3]} value={false}></Switch>
        <p class="text-xl">
          All
        </p>
      </div>
    </div>
  </div>
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

  .switches {
    width: 80%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .node {
    width: 100%;
    height: 100%;
    justify-content: center;
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
