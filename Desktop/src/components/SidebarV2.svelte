<script>
    import { location } from "svelte-spa-router";

    let routes = [
        {
            name: "Gallery",
            route: "#/gallery"
        },
        {
            name: "Upload",
            route: "#/upload"
        },
        {
            name: "Models",
            route: "#/models"
        },
        {
            name: "Help",
            route: "#/help"
        },
    ]

</script>

<div class="h-screen w-full bg-theme-blue-primary text-white">
    {#each routes as route}
        <div class="nav-item {("#" + $location) === route.route ? 'active' : ''}">
            <a href={route.route}>
                <div>{route.name}</div>
            </a>
        </div>
    {/each}
</div>

<style>
    .nav-item {
        display: flex;
        justify-content: center;
        padding: 10px 0 10px 0;
    }

    .active>a>div {
        color: blue;
    }
</style>
