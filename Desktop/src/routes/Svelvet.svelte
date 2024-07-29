<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ProcessingNode from "../components/ProcessingNode.svelte";
  import { Node, Svelvet, Minimap, Controls, Group, generateInput, generateOutput } from "svelvet";
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  let nodes = writable([
      { id: 'alpha', position: { x: 0, y: 0 }, bgColor: 'red', label: 'Default Node' },
      { id: 'beta', position: { x: 0, y: -50 }, bgColor: 'blue', label: 'Test 2nd' }
  ]);
  let nodeIdCounter = 2;

  let nodeTypes = [
      { type: 'Multiply', label: 'Multiply Unit', bgColor: 'lightblue' },
      { type: 'Divide', label: 'Divide Unit', bgColor: 'lightgreen' },
      { type: 'Add', label: 'Add Unit', bgColor: 'lightcoral' },
      { type: 'Subtract', label: 'Subtract Unit', bgColor: 'lightyellow' }
  ];

  function addNode(type) {
      const nodeType = nodeTypes.find(t => t.type === type);
      if (nodeType) {
          nodes.update(currentNodes => [
              ...currentNodes,
              { id: `node-${nodeIdCounter++}`, position: { x: Math.random() * 500, y: Math.random() * 500 }, bgColor: nodeType.bgColor, label: nodeType.label }
          ]);
      }
  }

  let test = generateInput({ value1: 5, value2: 10, option: 'default' });
</script>

<ProtectedRoutes>
  <div class="toolbar">
      <select on:change="{e => addNode(e.target.value)}">
          <option value="" disabled selected>Select Node Type</option>
          {#each nodeTypes as nodeType}
              <option value="{nodeType.type}">{nodeType.label}</option>
          {/each}
      </select>
  </div>
    <div>
        <button on:click={() => console.log("")}>Output Node</button>
    </div>  
  <div class="canvas">
      <Svelvet id="my-canvas" TD minimap controls editable>
        <Group color="lightblue" groupName="myGroup" position={{x: 500, y: 500}}  width={600} height={200}>
            <Node/>
            <Node />
        </Group>
            <Node label="Output" />
        <ProcessingNode/>
          {#each $nodes as node}
              <Node id={node.id} position={node.position} bgColor={node.bgColor} label={node.label} inputsStore={test} LR />
          {/each}
      </Svelvet>
  </div>
</ProtectedRoutes>

<style>
  .toolbar {
      margin: 10px;
      color: white;
  }

    .toolbar select {
        padding: 5px;
        font-size: 16px;
    }

    .toolbar option {
        color: black;
    }
  .canvas {
      width: 100%;
      height: 90%;
      display: flex;
      justify-content: center;
      border: 1px solid #ccc;
      margin-top: 10px;
  }
</style>
