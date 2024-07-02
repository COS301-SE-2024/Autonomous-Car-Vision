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

<div class="sidebarV2 h-full w-auto bg-theme-dark-background text-white">
    {#each routes as route}
        <div class="nav-item {("#" + $location) === route.route ? 'active' : ''}">
            <a href={route.route}>
                <div>{route.name}</div>
            </a>
        </div>
    {/each}
</div>

<style>
    .sidebarV2 {
        border-radius: 15px;
    }

    .nav-item {
        display: flex;
        justify-content: center;
        padding: 10px 0 10px 0;
    }

    .nav-item>a>div {
        opacity: 0.6;
    }

    .active>a>div {
        opacity: 1;
        color: white;
        font-weight: 600;
    }
</style>
