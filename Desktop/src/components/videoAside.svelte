<script>
    import { Avatar } from "svelte-materialify";

    export let AIinfo;
</script>

<div class="component">
    <div class="flex flex-row justify-between items-center text-white">
        <Avatar size="42px">
            <img
            src={AIinfo.img}
                alt={AIinfo.mName}
                />
            </Avatar>
        <a href="#/models">
            {AIinfo.mName}
        </a>
        <p>
            {AIinfo.mTime}
        </p>
    </div>
    <div class="line"></div>
</div>

<style>
    a:hover {
        text-decoration: underline;
    }

    .component {
        padding-bottom: 20px;
    }

    .line {
        border-left: 2px solid rgba(255, 255, 255, 0.6);
        height: 20px;
        position: absolute;
        left: 20px
    }
</style>