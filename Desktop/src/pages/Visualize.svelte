<script>
  import NetworkVisualizer from '../components/VisualizerComp.svelte'
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
</script>

<ProtectedRoutes >
  <div class="main">
    <h1> Interactive Network Visualizer</h1>
    <!-- <NetworkVisualizer /> -->
  </div> 
</ProtectedRoutes>

<style>
  .main {
    text-align: center;
    padding: 1em;
    max-width: 800px;
    margin: 0 auto;
  }

  h1 {
    color: #ffffff;
  }
</style>