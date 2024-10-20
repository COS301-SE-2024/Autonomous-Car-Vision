<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ProcessingNode from "../components/ProcessingNode.svelte";
  import { Svelvet, Node, Edge } from "svelvet";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import InputNode from "../components/InputNode.svelte";
  import OutputNode from "../components/OutputNode.svelte";
  import ThreeJS from "./ThreeJS.svelte";
  import { Button, Icon } from "svelte-materialify";
  import { mdiClose } from "@mdi/js";
  import { get } from "svelte/store";
  import { canvas } from "../stores/store";
  import toast, { Toaster } from "svelte-french-toast";
  import {theme} from '../stores/themeStore';

  let nodes = writable([]);
  let edges = writable([]);
  let savedCanvas;
  let savedCanvases = [];
  let nodeIdCounter = 0;

  let pipeRunModal = false;
  let preProcessImg =
    "https://media1.tenor.com/m/a0IapXcGUMYAAAAC/wheee-rally-car.gif";
  let postProcessImg =
    "https://media1.tenor.com/m/a0IapXcGUMYAAAAC/wheee-rally-car.gif";
  let dotPLYFile = "";

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
      type: "Infusr",
      label: "Infusr",
      bgColor: "white",
      operation: "infusr",
    },
    {
      type: "Taggr",
      label: "Taggr",
      bgColor: "blue",
      operation: "taggr",
    },
    {
      type: "Observer",
      label: "Observer",
      bgColor: "red",
      operation: "observer",
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
        position: { x: Math.random() * 500, y: Math.random() * 500 },
        component: ProcessingNode,
      };
      nodes.update((currentNodes) => {
        if (!Array.isArray(currentNodes)) {
          currentNodes = [];
        }
        return [...currentNodes, newNode];
      });
    }
  }

  function addSavedNodes(savedNodes, savedEdges) {
    return new Promise((resolve) => {
      const nodeMap = new Map();

      savedNodes.forEach((savedNode) => {
        let componentToUse;

        if (savedNode.operation === "input") {
          componentToUse = InputNode;
        } else if (savedNode.operation === "output") {
          componentToUse = OutputNode;
        } else {
          componentToUse = ProcessingNode;
        }

        const newNode = {
          id: savedNode.id,
          operation: savedNode.operation,
          label: savedNode.label,
          bgColor: savedNode.bgColor,
          position: savedNode.position || { x: 100, y: 100 },
          component: componentToUse,
          connectors: [],
        };

        nodeMap.set(savedNode.id, newNode);
      });

      nodes.update((currentNodes) => {
        if (!Array.isArray(currentNodes)) {
          currentNodes = [];
        }
        return [...currentNodes, ...Array.from(nodeMap.values())];
      });

      savedEdges.forEach((edge) => {
        const sourceNodeId = edge.sourceNode.id.replace(/^N-/, "");
        const targetNodeId = edge.targetNode.id.replace(/^N-/, "");

        const sourceNode = nodeMap.get(sourceNodeId);
        if (sourceNode && !sourceNode.connectors.includes(targetNodeId)) {
          sourceNode.connectors.push(targetNodeId);
        }
      });

      edges.update((currentEdges) => {
        if (!Array.isArray(currentEdges)) {
          currentEdges = [];
        }
        return [...currentEdges, ...savedEdges];
      });

      resolve();
    });
  }

  function SaveCanvas() {
    const currentNodes = get(nodes);
    const currentEdges = get(edges);
    const canvasState = { nodes: currentNodes, edges: currentEdges };
    const jsonParse = JSON.stringify(canvasState);

    canvas.set(jsonParse);

    savedCanvas = canvasState;
    savedCanvases = [...savedCanvases, canvasState];

    toast.success("Successfully saved your pipe!", {
      duration: 5000,
      position: "top-center",
    });

    encoder();

  }

  async function LoadCanvas() {
    const savedData = get(canvas);
    if (savedData) {
      const parsedData = JSON.parse(savedData);
      const { nodes: savedNodes, edges: savedEdges } = parsedData;

      const currentEdges = get(edges);

      nodes.set([]);

      if (Array.isArray(savedNodes)) {
        await addSavedNodes(savedNodes, savedEdges);
      }

      const mergedEdges = [
        ...currentEdges,
        ...savedEdges.filter((savedEdge) => {
          return !currentEdges.some(
            (currentEdge) =>
              currentEdge.sourceNode.id === savedEdge.sourceNode.id &&
              currentEdge.targetNode.id === savedEdge.targetNode.id,
          );
        }),
      ];

      edges.set(mergedEdges);
    } else {
      setCanvas();
    }
  }

  function ClearCanvas() {
    nodes.set([]);
    edges.set([]);
    setCanvas();
    toast.success("Successfully cleared the pipe!", {
      duration: 5000,
      position: "top-center",
    });
  }

  function handleEdgeConnect(event) {
    edges.update((currentEdges) => [
      ...currentEdges,
      {
        sourceAnchor: event.detail.sourceAnchor,
        sourceNode: event.detail.sourceNode,
        targetAnchor: event.detail.targetAnchor,
        targetNode: event.detail.targetNode,
      },
    ]);
  }

  function handleEdgeDisconnect(event) {
    edges.update((currentEdges) => {
      if (!Array.isArray(currentEdges)) {
        return [];
      }
      return currentEdges.filter(
        (edge) =>
          !(
            edge.sourceAnchor === event.detail.sourceAnchor &&
            edge.sourceNode.id === event.detail.sourceNode.id &&
            edge.targetAnchor === event.detail.targetAnchor &&
            edge.targetNode.id === event.detail.targetNode.id
          ),
      );
    });
  }

  function deleteNode(nodeId) {
    nodes.update((currentNodes) =>
      currentNodes.filter((node) => node.id !== nodeId),
    );
  }

  function generatePipeString(edges) {
    const adjacencyList = buildAdjacencyList(edges);
    const startNode = findStartNode(adjacencyList, edges);
    const orderedNodes = orderNodesByEdges(adjacencyList, startNode);
    return createPipeString(orderedNodes);
  }

  function validatePipe(pipeString) {
    const tokens = pipeString.split(",");

    let hasYoloUnit = false;
    let hasInfusrUnit = false;
    let hasTaggrUnit = false;
    let hasObserverUnit = false;
    if (
      tokens[0] !== "inputUnit" ||
      tokens[tokens.length - 1] !== "outputUnitTest.all"
    ) {
      toast.error(
        "Error: Pipe string must start with 'inputUnit' and end with 'outputUnit'.",
      );
      return false;
    }
    for (let i = 1; i < tokens.length - 1; i++) {
      const token = tokens[i];

      if (token.startsWith("yoloUnit")) {
        hasYoloUnit = true;
      } else if (token.startsWith("infusrUnit")) {
        hasInfusrUnit = true;
      } else if (token === "taggrUnit") {
        if (!hasYoloUnit || !hasInfusrUnit) {
          toast.error(
            "Error: taggrUnit must come after both a yoloUnit and an infusrUnit.",
          );
          return false;
        }
        hasTaggrUnit = true;
      } else if (token === "observerUnit") {
        if (!hasInfusrUnit) {
          toast.error(
            "Error: taggrUnit must come after both a yoloUnit and an infusrUnit.",
          );
          return false;
        }
        hasObserverUnit = true;
      }
    }

    if (hasTaggrUnit && (!hasYoloUnit || !hasInfusrUnit)) {
      toast.error(
        "Error: taggrUnit is present but either yoloUnit or infusrUnit is missing.",
      );
      return false;
    }

    return true;
  }

  async function encoder() {
    const pipe = generatePipeString($edges);

    const units = pipe.split(",").map((unit) => unit.replace(/^N-/, ""));
    
    if (units[0] !== "inputUnit" || units[units.length - 1] !== "outputUnit") {
      console.log("Units: ", units)
      toast.error(
        "Error: Pipe string must start with 'inputUnit' and end with 'outputUnit'.",
      );
      savedCanvas = null;
      console.log(pipe);
      return pipe;
    }

    const intermediateUnits = units.slice(1, -1);

    const labeledUnits = intermediateUnits.map((id) => {
      const node = savedCanvas.nodes.find(
        (n) => n.id.replace(/^N-/, "") === id,
      );
      if (node) {
        if (node.label.includes("Nano")) {
          return "yoloUnit.yolov8n";
        } else if (node.label.includes("Small")) {
          return "yoloUnit.yolov8s";
        }
        if (node.label.includes("Segmentation")) {
          return "yoloUnit.yolov8n-seg";
        }
        if(node.label.includes("Infusr")) {
          return "infusrUnit"
        }
        if(node.label.includes("Taggr")) {
          return "taggrUnit"
        }
        if(node.label.includes("Observer")) {
          return "observerUnit"
        }
        if (node.label.includes("High-Viz v1")) {
          return "HV1";
        }
      } else {
        console.error(`Error: No label found for node with ID ${id}.`);
        return "Unknown Node";
      }
    });

    const labeledPipeString = `inputUnit,${labeledUnits.join(",")},outputUnitTest.all`;

    const jsonPayload = JSON.stringify({ pipe: labeledPipeString });

    if (validatePipe(labeledPipeString)) {
      await window.electronAPI.savePipeJson(jsonPayload);
    } else {
      toast.error("Invalid pipe");
    }
  }

  function orderNodesByEdges(adjacencyList, startNode) {
    const orderedNodes = [];
    let currentNode = startNode;

    while (currentNode) {
      orderedNodes.push(currentNode);
      const neighbors = adjacencyList.get(currentNode);
      currentNode = neighbors ? neighbors[0] : null;
    }

    return orderedNodes;
  }

  function buildAdjacencyList(edges) {
    const adjacencyList = new Map();

    edges.forEach((edge) => {
      const sourceId = edge.sourceNode.id;
      const targetId = edge.targetNode.id;

      if (!adjacencyList.has(sourceId)) {
        adjacencyList.set(sourceId, []);
      }
      adjacencyList.get(sourceId).push(targetId);
    });

    return adjacencyList;
  }

  function findStartNode(adjacencyList, edges) {
    const allNodes = new Set();
    const nodesWithIncomingEdges = new Set();

    edges.forEach((edge) => {
      allNodes.add(edge.sourceNode.id);
      allNodes.add(edge.targetNode.id);
      nodesWithIncomingEdges.add(edge.targetNode.id);
    });

    for (const node of allNodes) {
      if (!nodesWithIncomingEdges.has(node)) {
        return node;
      }
    }
    return null;
  }

  function createPipeString(orderedNodes) {
    return orderedNodes.join(",");
  }

  function findNodeLabel(nodeID) {}

  function setCanvas() {
    const inputNode = {
      id: `inputUnit`,
      component: InputNode,
      label: "Input",
      position: { x: 100, y: 100 },
      operation: "input",
    };

    const outputNode = {
      id: `outputUnit`,
      component: OutputNode,
      label: "Output",
      position: { x: 1000, y: 100 },
      operation: "output",
    };

    nodes.set([inputNode, outputNode]);
  }

  function toggleRunModal() {
    pipeRunModal = !pipeRunModal;
  }

  function runPipe() {
    toggleRunModal();
  }

  onMount(() => {
    setCanvas();
    LoadCanvas();
  });
</script>



<ProtectedRoutes>
  <Toaster />
  {#if $theme === 'highVizLight'}
  <div class="toolbar flex flex-row justify-between">
    <div class="flex flex-row items-center gap-4 text-black">
      <p>Select an AI model</p>
      <select
        class="bg-dark-primary rounded-full text-dark-background text-center"
        on:change={(e) => addNode(e.target.value)}
      >
        <option value="" disabled selected>AI Models</option>
        {#each nodeTypes as nodeType}
          <option value={nodeType.type}>{nodeType.label}</option>
        {/each}
      </select>
    </div>
    <div class="flex flex-row gap-2">
      <Button
        rounded
        on:click={ClearCanvas}
        class="bg-dark-primary text-dark-background"
        >Clear Pipe
      </Button>
      <Button
        rounded
        on:click={SaveCanvas}
        class="bg-dark-primary text-dark-background"
        >Save Pipe
      </Button>
    </div>
  </div>
  <div class="canvasLight">
    <Svelvet
      fitView
      id="my-canvas"
      TD
      minimap
      editable={true}
      theme="highVizLight"
      on:connection={handleEdgeConnect}
      on:disconnection={handleEdgeDisconnect}
    >
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
  {#if pipeRunModal}
    <div class="runPipe w-2/4 h-2/5 p-6">
      <div>
        <Button text on:click={() => (pipeRunModal = !pipeRunModal)}>
          <Icon path={mdiClose} size={38}></Icon>
        </Button>
      </div>
      <div class="flex items-center h-full">
        <div class="w-full flex justify-between gap-10">
          <div class="inputImagePre">
            <h1 class="pb-10 text-3xl text-black text-center">
              Input
            </h1>
            <img class="rounded-xl" src={preProcessImg} alt={preProcessImg} />
          </div>
          <div class="outputImagePost">
            <h1 class="pb-10 text-3xl text-black text-center">
              Output
            </h1>
            <img class="rounded-xl" src={postProcessImg} alt={postProcessImg} />
          </div>
        </div>
      </div>
    </div>
  {/if}
  {:else}
  <div class="toolbar flex flex-row justify-between">
    <div class="flex flex-row items-center gap-4">
      <p>Select an AI model</p>
      <select
        class="bg-dark-primary rounded-full text-dark-background text-center"
        on:change={(e) => addNode(e.target.value)}
      >
        <option value="" disabled selected>AI Models</option>
        {#each nodeTypes as nodeType}
          <option value={nodeType.type}>{nodeType.label}</option>
        {/each}
      </select>
    </div>
    <div class="flex flex-row gap-2">
      <Button
        rounded
        on:click={ClearCanvas}
        class="bg-dark-primary text-dark-background"
        >Clear Pipe
      </Button>
      <Button
        rounded
        on:click={SaveCanvas}
        class="bg-dark-primary text-dark-background"
        >Save Pipe
      </Button>
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
  {#if pipeRunModal}
    <div class="runPipe w-2/4 h-2/5 p-6">
      <div>
        <Button text on:click={() => (pipeRunModal = !pipeRunModal)}>
          <Icon path={mdiClose} size={38}></Icon>
        </Button>
      </div>
      <div class="flex items-center h-full">
        <div class="w-full flex justify-between gap-10">
          <div class="inputImagePre">
            <h1 class="pb-10 text-3xl text-black text-center">
              Input
            </h1>
            <img class="rounded-xl" src={preProcessImg} alt={preProcessImg} />
          </div>
          <div class="outputImagePost">
            <h1 class="pb-10 text-3xl text-black text-center">
              Output
            </h1>
            <img class="rounded-xl" src={postProcessImg} alt={postProcessImg} />
          </div>
        </div>
      </div>
    </div>
  {/if}
  {/if}

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

   .canvasLight {
    width: 100%;
    height: 90%;
    display: flex;
    justify-content: center;
    border: 1px solid #ccc;
    margin-top: 10px;
  }

  .runPipe {
    background-color: #ccccccc0;
    border-radius: 12px;
    position: fixed;
    top: 50%;
    left: 55%;
    transform: translate(-55%, -50%);
  }
</style>
