<script>
  import NetworkVisualizer from '../components/VisualizerComp.svelte'
  import ProtectedRoutes from "../routes/ProtectedRoutes.svelte";
  import { writable } from 'svelte/store';

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
    /* max-width: 800px; */
    margin: 0 auto;
  }
</style>