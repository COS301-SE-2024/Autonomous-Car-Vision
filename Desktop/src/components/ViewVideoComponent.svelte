<script>
    import { onMount } from "svelte";

    let time = 0;
    let duration;
    let paused = true;

    let showControls = true;
    let showControlsTimeout;

    function format(seconds) {
        if (isNaN(seconds)) return "...";

        const minutes = Math.floor(seconds / 60);
        seconds = Math.floor(seconds % 60);
        if (seconds < 10) seconds = "0" + seconds;

        return `${minutes}:${seconds}`;
    }

    let lastMouseDown;

    function handleMove(e) {
        clearTimeout(showControlsTimeout);
        showControlsTimeout = setTimeout(() => (showControls = false), 2500);
        showControls = true;

        if (!duration) return;
        if (e.type !== "touchmove" && !(e.buttons & 1)) return;

        const clientX =
            e.type === "touchmove" ? e.touches[0].clientX : e.clientX;
        const { left, right } = this.getBoundingClientRect();
        time = (duration * (clientX - left)) / (right - left);
    }

    function handleMousedown(e) {
        lastMouseDown = new Date();
    }

    function handleMouseup(e) {
        if (new Date() - lastMouseDown < 300) {
            if (paused) e.target.play();
            else e.target.pause();
        }
    }

    let thumbnailBar;
    let interval = 20; // Extract a frame every 20 seconds
    let frames = [];
    let videoPath = "https://sveltejs.github.io/assets/caminandes-llamigos.mp4";


    async function extractFrames() {
        try {
            frames = await window.electronAPI.extractFrames(
                videoPath,
                interval,
            );
        } catch (error) {
            console.error("Error extracting frames:", error);
        }
    }

    onMount(() => {
        extractFrames();
    });

    function seekToFrame(framePath) {
        const index = frames.indexOf(framePath);
        currentTime = index * 10; // Adjust according to the interval
        console.log("Seek to frame:", framePath);
    }
</script>

<div>
    <video
        poster="https://sveltejs.github.io/assets/caminandes-llamigos.jpg"
        src={videoPath}
        on:mousemove={handleMove}
        on:touchmove|preventDefault={handleMove}
        on:mousedown={handleMousedown}
        on:mouseup={handleMouseup}
        bind:currentTime={time}
        bind:duration
        bind:paused
    >
        <track kind="captions" />
    </video>
    <div class="controls" style="opacity: {duration && showControls ? 1 : 0}">
        <progress value={time / duration || 0} />
        <div class="info">
            <span class="time">{format(time)}</span>
            <span
                >click anywhere to {paused ? "play" : "pause"} / drag to seek</span
            >
            <span class="time">{format(duration)}</span>
        </div>
    </div>
</div>
<div bind:this={thumbnailBar} class="thumbnail-bar">
    {#each frames as frame}
        <div
            class="thumbnail"
            style="background-image: url({frame})"
            on:click={() => seekToFrame(frame)}
            on:keydown
        ></div>
    {/each}
</div>

<style>
    .thumbnail-bar {
        display: flex;
        /* overflow-x: scroll; */
        /* overflow-y: hidden; */
        height: 100px;
        width: 100%;
    }

    .thumbnail {
        flex: 0 0 auto;
        width: 120px;
        height: 100px;
        background-size: cover;
        background-position: center;
    }

    div {
        position: relative;
    }

    .controls {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: opacity 1s;
    }

    .info {
        display: flex;
        width: 100%;
        justify-content: space-between;
    }

    span {
        padding: 0.2em 0.5em;
        color: white;
        text-shadow: 0 0 8px black;
        font-size: 1.4em;
        opacity: 0.7;
    }

    .time {
        width: 3em;
    }

    .time:last-child {
        text-align: right;
    }

    progress {
        display: block;
        width: 100%;
        height: 40px;
        position: absolute;
        bottom: 0;
        -webkit-appearance: none;
        appearance: none;
    }

    progress::-webkit-progress-bar {
        background-color: rgba(0, 0, 0, 0.2);
    }

    progress::-webkit-progress-value {
        background-color: rgba(255, 255, 255, 0.6);
    }

    video {
        width: 100%;
    }
</style>
