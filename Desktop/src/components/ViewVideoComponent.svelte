<script>
    import { onMount } from "svelte";

    export let videoPath = "";
    videoPath = "https://sveltejs.github.io/assets/caminandes-llamigos.mp4";

    let time = 0;
    let volume = 0;
    let duration;
    let paused = true;

    let showControls = true;
    let showControlsTimeout;

    let thumbnailBar;
    let interval = 10; // Extract a frame every 10 seconds
    let frames = [];

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

        // Find the frame index that corresponds to the current time
        const frameIndex = Math.floor(time / interval);
        const frameElement =
            document.querySelectorAll(".thumbnail")[frameIndex];
        if (frameElement) {
            frameElement.scrollIntoView({
                behavior: "smooth",
                block: "nearest",
                inline: "center",
            });
        }
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

    async function extractFrames() {
        try {
            const framePaths = await window.electronAPI.extractFrames(
                videoPath,
                interval
            );
            frames = framePaths.map(framePath => framePath.replace(/\\/g, '/')); // Convert backslashes to slashes for URLs
        } catch (error) {
            console.error("Error extracting frames:", error);
        }
    }

    onMount(() => {
        extractFrames();
    });

    function seekToFrame(framePath) {
        const index = frames.indexOf(framePath);
        time = index * interval; // Adjust according to the interval
        console.log("Seek to frame:", framePath);
        showControls = true;

        // Scroll the clicked frame into the center of the thumbnail bar
        const frameElement = document.querySelectorAll(".thumbnail")[index];
        if (frameElement) {
            frameElement.scrollIntoView({
                behavior: "smooth",
                block: "nearest",
                inline: "center",
            });
        }
    }

    function pause() {
        paused = !paused;
        console.log(frames);
    }

</script>
<div>
    <div>
        <!-- poster="https://sveltejs.github.io/assets/caminandes-llamigos.jpg" -->
        <video
            src={videoPath}
            on:mousemove={handleMove}
            on:touchmove|preventDefault={handleMove}
            on:mousedown={handleMousedown}
            on:mouseup={handleMouseup}
            bind:currentTime={time}
            bind:duration
            bind:paused
            bind:volume={volume}
            class="w-full"
        >
            <track kind="captions" />
        </video>
        <div class="controls" style="opacity: {duration && showControls ? 1 : 0}">
            <progress class="TimelineProgress" value={time / duration || 0} />
            <button class="pl-4 w-16 border-2 border-white rounded-full text-white font-bold" on:click={pause}>
                {paused ? "Play" : "Pause"} 
                <!-- WILL ADD SVG JUST FOR NOW LEAVING IT AS TEXT -->
            </button>
            <div class="info">
                <span class="time">{format(time)}</span>
                <span>:</span>
                <!-- <span>click anywhere to {paused ? "play" : "pause"} / drag to seek</span> -->
                <span class="time">{format(duration)}</span>
            </div>

        </div>
    </div>
    <div bind:this={thumbnailBar} class="thumbnail-bar">
        {#each frames as frame}
            <div
                class="thumbnail hover:cursor-pointer"
                style="background-image: url({frame})"
                on:click={() => seekToFrame(frame)}
                on:keypress
            ></div>
        {/each}
    </div>
</div>

<style>
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
        background: #888;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    .thumbnail-bar {
        display: flex;
        overflow-x: scroll;
        overflow-y: hidden;
        height: 100px;
    }

    .thumbnail {
        flex: 0 0 auto;
        width: 120px;
        height: 100px;
        background-size: cover;
        background-position: center;
        cursor: pointer;
    }

    .thumbnail:hover {
        transform: scale(1.1);
        transition: linear 0.2s;
    }

    div {
        position: relative;
    }

    .controls {
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: center;
        position: absolute;
        bottom: 0;
        gap: 2rem;
        width: 100%;
        transition: opacity 0.5s;
    }

    .TimelineProgress {
        position: absolute;
        bottom: 40px;
        left: 0;
        width: 100%;
        height: 5px;
    }

    .info {
        display: flex;
        width: fit-content;
        justify-content: center;
    }

    span {
        padding: 0.2em 0.2em;
        color: white;
        text-shadow: 0 0 8px black;
        font-size: 1.4em;
        opacity: 0.7;
    }

    .time {
        width: fit-content;
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
        background-color: rgb(255, 255, 255);
    }

    progress::-webkit-progress-value {
        background-color: #ff1f1fb2;
    }

    video {
        width: 100%;
    }
</style>