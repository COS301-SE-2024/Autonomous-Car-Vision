<script>
    import { onMount } from 'svelte';
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";;
 
</script>


    
<div class="relative h-screen flex justify-center items-center bg-gray-100">
 <webview
  id="visualizer"
  title="Netron App"
  src="https://netron.app"/>
</div>
  


  <style>
  webview{
    border: 1px solid rgb(255, 255, 255);
    width: 100%;
    height: 85%;
  }
  </style>
  
  
  