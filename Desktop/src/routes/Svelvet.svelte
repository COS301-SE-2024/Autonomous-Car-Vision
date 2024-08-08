<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ProcessingNode from "../components/ProcessingNode.svelte";
  import { Svelvet, Node } from "svelvet";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import InputNode from "../components/InputNode.svelte";
  import OutputNode from "../components/OutputNode.svelte";
  import { Button } from "svelte-materialify";
  import { get } from "svelte/store";

  let nodes = writable([]);
  let edges = writable([])
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
      nodes.update((currentNodes) => {
        if (!Array.isArray(currentNodes)) {
          currentNodes = [];
        }
        return [...currentNodes, newNode];
      });
    }
    nodes.subscribe((value) => {
      console.log(value);
    });
  }

  function saveCanvas() {
    const currentNodes = get(nodes);
    const currentEdges = get(edges);
    const canvasState = { nodes: currentNodes, edges: currentEdges };
    const jsonCanvasState = JSON.stringify(canvasState);

    localStorage.setItem('canvasData', jsonCanvasState);

    console.log("Canvas Saved", canvasState);

  }

  function loadCanvas() {
    const savedData = localStorage.getItem('canvasData');
    console.log(savedData)
    if (savedData) {
      const { nodes: savedNodes, edges: savedEdges } = JSON.parse(savedData);
      nodes.set(savedNodes || []);
      edges.set(savedEdges || []);
    }
  }

  // function to handle when a node gets a connection
  function handleEdgeConnect(event) {
    edges.update((currentEdges) => [
      ...currentEdges,
      {
        source: event.detail.source,
        target: event.detail.target,
      },
    ]);
    console.log("Edge Connected", event.detail);
  }

  // function to handle when a node loses a connection
  function handleEdgeDisconnect(event) {
    edges.update((currentEdges) =>
      currentEdges.filter(
        (edge) =>
          !(edge.source === event.detail.source && edge.target === event.detail.target)
      )
    );
  }


  onMount(() => {
    localStorage.clear();
    loadCanvas();
  })

  // Add a check that the user has to save the canvas before leaving the page if they have any unsaved changes
  // add another check that the user has to save the canvas before running it
  // make the sidebar a drawer that shows all the saved canvases
</script>

<ProtectedRoutes>
  <div class="toolbar flex flex-row justify-between">
    <select on:change={(e) => addNode(e.target.value)}>
      <option value="" disabled selected>Select Node Type</option>
      {#each nodeTypes as nodeType}
        <option value={nodeType.type}>{nodeType.label}</option>
      {/each}
    </select>
    <div class="flex flex-row gap-2">
      <Button on:click={loadCanvas} class="bg-dark-primary text-dark-background">Load Prev</Button>
      <Button on:click={saveCanvas} class="bg-dark-primary text-dark-background">Save</Button>
    </div>
  </div>
  <div class="canvas">
    <Svelvet
      fitView
      id="my-canvas"
      TD
      minimap
      editable={true}
      theme="dark"
      on:connection={handleEdgeConnect}
      on:disconnection={handleEdgeDisconnect}
    >
      <!-- <Drawer /> -->
      <InputNode
        identifier="inputNode"
        operation="input"
        label="Input Image"
        position={{ x: 0, y: 0 }}
      />
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
