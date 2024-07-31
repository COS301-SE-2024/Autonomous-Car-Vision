<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ProcessingNode from "../components/ProcessingNode.svelte";
  import {
    Node,
    Svelvet,
  } from "svelvet";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  let nodes = writable([
    {
      id: "sourceNode",
      position: { x: 1000, y: 300 },
      bgColor: "red",
      label: "Node id: sourceNode",
    },
    {
      id: "targetNode",
      position: { x: 1000, y: 500 },
      bgColor: "blue",
      label: "Result id: targetNode",
    },
  ]);
  let nodeIdCounter = 2;

  let nodeTypes = [
    { type: "Multiply", label: "Multiply Unit", bgColor: "lightblue" },
    { type: "Divide", label: "Divide Unit", bgColor: "lightgreen" },
    { type: "Add", label: "Add Unit", bgColor: "lightcoral" },
    { type: "Subtract", label: "Subtract Unit", bgColor: "lightyellow" },
  ];

  function addNode(type) {
    const nodeType = nodeTypes.find((t) => t.type === type);
    if (nodeType) {
      nodes.update((currentNodes) => [
        ...currentNodes,
        {
          id: `node-${nodeIdCounter++}`,
          position: { x: Math.random() * 500, y: Math.random() * 500 },
          bgColor: nodeType.bgColor,
          label: nodeType.label,
        },
      ]);
    }
  }

</script>

<ProtectedRoutes>
  <div class="toolbar">
    <select on:change={(e) => addNode(e.target.value)}>
      <option value="" disabled selected>Select Node Type</option>
      {#each nodeTypes as nodeType}
        <option value={nodeType.type}>{nodeType.label}</option>
      {/each}
    </select>
  </div>
  <div class="canvas">
    <Svelvet fitView id="my-canvas" TD minimap controls editable>
      <ProcessingNode
        connectors={["processingNode"]}
        Identifier="inputNode"
        position={{ x: 0, y: 200 }}
      />
      <ProcessingNode
        connectors={["processingNode"]}
        Identifier="inputNode1"
        position={{ x: 0, y: 400 }}
      />
      <ProcessingNode
        connectors={["sourceNode", "targetNode"]}
        Identifier="processingNode"
        position={{ x: 485, y: 315 }}
      />
      {#each $nodes as node}
        <Node
          id={node.id}
          position={node.position}
          bgColor={node.bgColor}
          label={node.label}
          LR
        />
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
