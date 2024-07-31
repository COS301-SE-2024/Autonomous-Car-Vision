<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ProcessingNode from "../components/ProcessingNode.svelte";
  import { Node, Svelvet } from "svelvet";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import InputNode from "../components/InputNode.svelte";
  import OutputNode from "../components/OutputNode.svelte";

  let nodes = writable([]);
  let nodeIdCounter = 301;

  let nodeTypes = [
    {
      type: "YoloV8n",
      label: "YOLO V8 Nano",
      bgColor: "lightblue",
      operation: "yolonano",
    },
    {
      type: "YoloV8s",
      label: "YOLO V8 Small",
      bgColor: "lightgreen",
      operation: "yolosmall",
    },
    {
      type: "YoloV8segg",
      label: "YOLO V8 Segmentation",
      bgColor: "lightcoral",
      operation: "yoloseg",
    },
    {
      type: "HV1",
      label: "High-Viz v1",
      bgColor: "lightyellow",
      operation: "hv1",
    },
  ];

  function addNode(type) {
    const nodeType = nodeTypes.find((t) => t.type === type);
    if (nodeType) {
      const newNode = {
        id: `node-${nodeIdCounter++}`,
        operation: nodeType.operation,
        label: nodeType.label,
        bgColor: nodeType.bgColor,
        position: { x: Math.random() * 500, y: Math.random() * 500 }, // Set a random position
        component: ProcessingNode,
      };

      nodes.update((currentNodes) => [...currentNodes, newNode]);
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
      <InputNode
        identifier="inputNode"
        operation="input"
        label="Input Image"
        position={{ x: 0, y: 0 }}
      />
      <!-- <ProcessingNode
        connectors={["processingNode"]}
        identifier="inputNode"
        operation="add"
        label="Add"
        position={{ x: 0, y: 200 }}
      />
      <ProcessingNode
        connectors={["processingNode"]}
        identifier="inputNode1"
        operation="multiply"
        label="Multiply"
        position={{ x: 0, y: 400 }}
      />
      <ProcessingNode
        connectors={["Output"]}
        identifier="processingNode"
        operation="add"
        label="Add"
        position={{ x: 485, y: 315 }}
      /> -->
      <OutputNode identifier="Output" position={{ x: 1000, y: 315 }} />
      {#each $nodes as node}
        <svelte:component
          this={node.component}
          id={node.id}
          identifier={node.id}
          operation={node.operation}
          bgColor={node.bgColor}
          label={node.label}
          position={node.position}
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
