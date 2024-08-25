<script>
  import ProtectedRoutes from "./ProtectedRoutes.svelte";
  import ProcessingNode from "../components/ProcessingNode.svelte";
  import { Svelvet, Node, Edge } from "svelvet";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import InputNode from "../components/InputNode.svelte";
  import OutputNode from "../components/OutputNode.svelte";
  import ThreeJS from "./ThreeJS.svelte";
  import { Button, Icon, Tooltip } from "svelte-materialify";
  import { mdiClose } from "@mdi/js";
  import { get } from "svelte/store";
  import { canvas } from "../stores/store";
  import toast, { Toaster } from "svelte-french-toast";
  import { push } from "svelte-spa-router";
  import QuantamLoader from "../components/QuantamLoader.svelte";
  import { outputPipe } from "../stores/store";

  let nodes = writable([]);
  let edges = writable([]);
  let savedCanvas;
  let savedCanvases = [];
  let nodeIdCounter = 0;
  let runningPipe = false;

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
  }

  function addSavedNodes(savedNodes, savedEdges) {
    return new Promise((resolve) => {
      // Create a map of node ID to node configuration
      const nodeMap = new Map();

      savedNodes.forEach((savedNode) => {
        let componentToUse;

        // Determine which component to use based on the saved node's component
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
          position: savedNode.position || { x: 100, y: 100 }, // Default position if none
          component: componentToUse,
          connectors: [], // Initialize connectors array
        };

        nodeMap.set(savedNode.id, newNode);
      });

      // Add nodes to the store
      nodes.update((currentNodes) => {
        if (!Array.isArray(currentNodes)) {
          currentNodes = [];
        }
        return [...currentNodes, ...Array.from(nodeMap.values())];
      });

      // Update connectors based on edges
      savedEdges.forEach((edge) => {
        console.log(nodeMap);
        const sourceNodeId = edge.sourceNode.id.replace(/^N-/, "");
        const targetNodeId = edge.targetNode.id.replace(/^N-/, "");

        const sourceNode = nodeMap.get(sourceNodeId);
        if (sourceNode && !sourceNode.connectors.includes(targetNodeId)) {
          // console.log(sourceNode.connectors);
          sourceNode.connectors.push(targetNodeId);
          // console.log(sourceNode.connectors);
        }
      });

      // Add edges to the store
      edges.update((currentEdges) => {
        if (!Array.isArray(currentEdges)) {
          currentEdges = [];
        }
        return [...currentEdges, ...savedEdges];
      });

      // Resolve the promise after nodes and edges are added
      resolve();
    });
  }

  function SaveCanvas() {
    const currentNodes = get(nodes);
    const currentEdges = get(edges);
    if (currentNodes.length == 2) {
      toast.error("Please add units to your pipe!", {
        duration: 5000,
        position: "top-center",
      });
      return;
    }
    if (currentEdges < 1) {
      toast.error("Please create a pipe before saving!", {
        duration: 5000,
        position: "top-center",
      });
      return;
    }
    console.log("EDGES: ", currentEdges);
    const canvasState = { nodes: currentNodes, edges: currentEdges };
    const jsonParse = JSON.stringify(canvasState);

    console.log("NODES: ", JSON.parse(jsonParse).nodes);

    canvas.set(jsonParse);

    savedCanvas = canvasState;
    savedCanvases = [...savedCanvases, canvasState];

    console.log("Canvas Saved", canvasState);
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

      // Get the current edges from the store
      const currentEdges = get(edges);

      // Clear current nodes
      nodes.set([]);

      // Add saved nodes
      if (Array.isArray(savedNodes)) {
        await addSavedNodes(savedNodes, savedEdges);
      }

      // Merge current edges with saved edges, avoiding duplicates
      const mergedEdges = [
        ...currentEdges, // Retain existing edges
        ...savedEdges.filter((savedEdge) => {
          return !currentEdges.some(
            (currentEdge) =>
              currentEdge.sourceNode.id === savedEdge.sourceNode.id &&
              currentEdge.targetNode.id === savedEdge.targetNode.id,
          );
        }), // Add new edges from saved data
      ];

      // Update the edges store with merged edges
      edges.set(mergedEdges);

      console.log("Updated Nodes:", get(nodes));
      console.log("Updated Edges:", get(edges));
    } else {
      // If no saved data is found, reset the canvas to the default state
      setCanvas();
    }
  }

  function ClearCanvas() {
    nodes.set([]); // set nodes array empty
    edges.set([]); // set edges array empty
    setCanvas();
    toast.success("Successfully cleared the pipe!", {
      duration: 5000,
      position: "top-center",
    });
  }

  // function to handle when a node gets a connection
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

  // function to handle when a node loses a connection
  function handleEdgeDisconnect(event) {
    edges.update((currentEdges) => {
      if (!Array.isArray(currentEdges)) {
        return []; // Ensure we start with an empty array if currentEdges is not valid
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
    if (
      tokens[0] !== "inputUnit" ||
      !tokens[tokens.length - 1].includes("outputUnit")
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
    console.log("Generated Pipe:", pipe);

    const units = pipe.split(",").map((unit) => unit.replace(/^N-/, ""));

    if (units[0] !== "inputUnit" || units[units.length - 1] !== "outputUnit") {
      toast.error(
        "Error: Pipe string must start with 'inputUnit' and end with 'outputUnit'.",
      );
      savedCanvas = null;
      return;
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
          return "yoloUnit.yolov8n-seg"; // JUST USING v8n for this example
        }
        if (node.label.includes("High-Viz v1")) {
          return "HV1";
        }
      } else {
        console.error(`Error: No label found for node with ID ${id}.`);
        return "Unknown Node"; // Handle the case where the node is not found
      }
    });

    let labeledPipeString = `inputUnit,${labeledUnits.join(",")},outputUnit`;

    if ($outputPipe[3]) {
      labeledPipeString += ".all";
    }
    if ($outputPipe[0]) {
      labeledPipeString += ".lidar";
    }
    if ($outputPipe[1]) {
      labeledPipeString += ".bb";
    }
    if ($outputPipe[2]) {
      labeledPipeString += ".taggr";
    }

    console.log("Labeled Pipe String:", labeledPipeString);
    // Convert to JSON string
    const jsonPayload = JSON.stringify({ pipe: labeledPipeString });

    if (validatePipe(labeledPipeString)) {
      await window.electronAPI.savePipeJson(jsonPayload);
      // warp_pipe.set(labeledPipeString);
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
      currentNode = neighbors ? neighbors[0] : null; // Assuming single outgoing edge for simplicity
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
    return null; // No start node found
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
      position: { x: 100, y: 100 }, // Customize the position
      operation: "input",
    };

    const outputNode = {
      id: `outputUnit`,
      component: OutputNode,
      label: "Output",
      position: { x: 1000, y: 100 }, // Customize the position
      operation: "output",
    };

    // Add the nodes to the writable store
    nodes.set([inputNode, outputNode]);
  }

  async function spawnP() {
    const appPath = await window.electronAPI.getAppPath();
    const appDirectory = await window.electronAPI.resolvePath(appPath, "..");
    let scriptPath = `${appDirectory}/Process/pipe4/bobTheBuilder.py`;
    // const dirPath = `${appDirectory}/Desktop/testData`;
    window.electronAPI.runPythonScript2(scriptPath);
  }

  async function runPipe() {
    runningPipe = true;
    // RUN PIPE

    await spawnP();

    // Send to WarpPipe Page
    runningPipe = false;
    push("/warp_pipe");
  }

  onMount(() => {
    setCanvas();
    LoadCanvas();
  });
</script>

<ProtectedRoutes>
  <Toaster />
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
    <div class="flex flex-row gap-2 items-center">
      <!-- <Button on:click={LoadCanvas} class="bg-dark-primary text-dark-background"
              >Load Prev</Button
            > -->
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
      {#if savedCanvas}
        <Button
          rounded
          on:click={runPipe}
          class="bg-dark-primary text-dark-background cursor-default"
        >
          {#if runningPipe}
            <QuantamLoader />
          {:else}
            Run Pipe
          {/if}
        </Button>
      {:else}
        <Button disabled rounded class="bg-dark-primary text-dark-background"
          >Run Pipe
        </Button>
      {/if}
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
