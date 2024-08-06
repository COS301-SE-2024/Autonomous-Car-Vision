<script>
    import { onMount } from 'svelte';
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";;
    import * as d3 from 'd3';
    
      
    const data = {
    nodes: [
      { id: 'inputLayer', group: 1 },
      { id: 'hiddenLayer1_node1', group: 2 },
      { id: 'hiddenLayer1_node2', group: 2 },
      { id: 'hiddenLayer1_node3', group: 2 },
      { id: 'hiddenLayer2_node1', group: 3 },
      { id: 'hiddenLayer2_node2', group: 3 },
      { id: 'hiddenLayer2_node3', group: 3 },
      { id: 'hiddenLayer2_node4', group: 3 },
      { id: 'outputLayer', group: 4 }
    ],
    links: [
      { source: 'inputLayer', target: 'hiddenLayer1_node1', value: 1 },
      { source: 'inputLayer', target: 'hiddenLayer1_node2', value: 1 },
      { source: 'inputLayer', target: 'hiddenLayer1_node3', value: 1 },
      { source: 'hiddenLayer1_node1', target: 'hiddenLayer2_node1', value: 1 },
      { source: 'hiddenLayer1_node1', target: 'hiddenLayer2_node2', value: 1 },
      { source: 'hiddenLayer1_node2', target: 'hiddenLayer2_node2', value: 1 },
      { source: 'hiddenLayer1_node2', target: 'hiddenLayer2_node3', value: 1 },
      { source: 'hiddenLayer1_node3', target: 'hiddenLayer2_node3', value: 1 },
      { source: 'hiddenLayer1_node3', target: 'hiddenLayer2_node4', value: 1 },
      { source: 'hiddenLayer2_node1', target: 'outputLayer', value: 1 },
      { source: 'hiddenLayer2_node2', target: 'outputLayer', value: 1 },
      { source: 'hiddenLayer2_node3', target: 'outputLayer', value: 1 },
      { source: 'hiddenLayer2_node4', target: 'outputLayer', value: 1 }
    ]
  };

  onMount(() => {
    const svg = d3.select('svg');
    const width = +svg.attr('width');
    const height = +svg.attr('height');

    // Create a map of node IDs to node objects
    const nodeMap = new Map(data.nodes.map(node => [node.id, node]));

    // Update the links to reference node objects
    data.links.forEach(link => {
      link.source = nodeMap.get(link.source);
      link.target = nodeMap.get(link.target);
    });

    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(data.links)
      .enter().append('line')
      .attr('stroke-width', d => Math.sqrt(d.value));

    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(data.nodes)
      .enter().append('circle')
      .attr('r', 5)
      .attr('fill', d => color(d.group))
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    node.append('title')
      .text(d => d.id);

    simulation
      .nodes(data.nodes)
      .on('tick', ticked);

    simulation.force('link')
      .links(data.links);

    function ticked() {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    }

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    function color(group) {
      const scale = d3.scaleOrdinal(d3.schemeCategory10);
      return scale(group);
    }
  });
</script>


    
  <svg width="960" height="600"></svg>
  


  <style>
    .links line {
      stroke: #999;
      stroke-opacity: 0.6;
    }
  
    .nodes circle {
      stroke: #fff;
      stroke-width: 1.5px;
    }
  </style>
  
  
  