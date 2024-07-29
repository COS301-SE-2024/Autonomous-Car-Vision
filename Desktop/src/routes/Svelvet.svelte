<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { Node, Svelvet, Minimap, Controls } from "svelvet";
  </script>
  
  <ProtectedRoutes>
    <div class="canvas">
      <Svelvet id="my-canvas" TD minimap controls locked editable>
        <Node />
        <Node id="alpha" position="0, 0" bgColor="red" label="Default Node" />
        <Node id="beta" position="0, -50" bgColor="blue" label="Test 2nd" />
      </Svelvet>
    </div>
  </ProtectedRoutes>
  
  <style>
    .canvas {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
    }
  </style>
  