<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import ViewVideoComponent from "../components/ViewVideoComponent.svelte";

    export const videoURL = "";
</script>

<ProtectedRoutes>
    <ViewVideoComponent videoPath={videoURL}/>
</ProtectedRoutes>
