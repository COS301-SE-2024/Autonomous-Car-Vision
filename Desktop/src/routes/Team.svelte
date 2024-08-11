<script>
import ProtectedRoutes from "./ProtectedRoutes.svelte";

import { Svelvet, Node } from 'svelvet';
</script>

<ProtectedRoutes>
    <div class="team">
    </div>
    <Svelvet theme="dark">
        <Node/>
        <Node bgColor="red" label="Node" />
    </Svelvet>
</ProtectedRoutes>