<script>
    import { onMount } from 'svelte';
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";;
 
</script>


    
<div class="relative h-screen flex justify-center items-center bg-gray-100">
 <iframe
  id="visualizer"
  title="Netron App"
  src="https://netron.app"/> 
</div>
  


  <style>
  iframe{
    border: 1px solid black;
    width: 100%;
    height:90%;
    border-radius: 8px;
  }
  </style>
  
  
  