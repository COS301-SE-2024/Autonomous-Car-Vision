<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import ViewVideoComponent from "../components/ViewVideoComponent.svelte";
</script>

<ProtectedRoutes>
    <ViewVideoComponent />
</ProtectedRoutes>
