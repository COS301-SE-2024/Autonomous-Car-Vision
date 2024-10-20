<script>
  import NetworkVisualizer from '../components/VisualizerComp.svelte'
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
</script>

<ProtectedRoutes >
  <div class="main w-7/8 h-4/6">
    <NetworkVisualizer/>
  </div> 
</ProtectedRoutes>

<style>
  .main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }
</style>