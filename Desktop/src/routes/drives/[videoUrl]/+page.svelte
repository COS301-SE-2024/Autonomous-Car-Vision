<script>
    import ProtectedRoutes from "../../ProtectedRoutes.svelte";
    import Router, { push, location } from "svelte-spa-router";
    import ApexCharts from "apexcharts";
    import { onMount } from "svelte";
    import { Icon, Tooltip } from "svelte-materialify";
    import { mdiArrowLeft, mdiPlay } from "@mdi/js";
    import { DotLottieSvelte } from "@lottiefiles/dotlottie-svelte";
    import { VideoURL, OriginalVideoURL } from "../../../stores/video";
    import { originalVideoURL } from "../../../stores/processing";

    const drive = {
        length: 210,
        frame_count: 471,
        inferences: 221,
        FPS: 10,
        videourl: "test",
    };

    let videoPath;
    let chartInferences, chartFPS;
    let dotLottie1, dotLottie2, dotLottie3;
    let lottieElement1, lottieElement2, lottieElement3;

    function playLottie(lottie) {
        lottie?.play();
    }

    function pauseLottie(lottie) {
        lottie?.pause();
    }

    onMount(() => {
        videoPath = $location.replace("/drive/", "");
        videoPath = decodeURIComponent(videoPath);
        console.log(videoPath);
        drive.videourl = videoPath;
        console.log(drive.videourl);

        const inferencesOptions = {
            chart: {
                type: "line",
                height: 80,
                sparkline: {
                    enabled: true,
                },
            },
            series: [
                {
                    data: [5, 15, 10, 20, 30, 25, 35, 40, 50],
                },
            ],
            stroke: {
                curve: "smooth",
            },
            tooltip: {
                custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                    return (
                        "<div class='text-black'>" +
                        series[seriesIndex][dataPointIndex] +
                        "</div>"
                    );
                },
            },
        };

        const fpsOptions = {
            chart: {
                type: "line",
                height: 80,
                sparkline: {
                    enabled: true,
                },
            },
            series: [
                {
                    data: [60, 62, 70, 55, 50, 49, 50, 50, 46],
                },
            ],
            stroke: {
                curve: "smooth",
            },
            tooltip: {
                custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                    return (
                        "<div class='text-black'>" +
                        series[seriesIndex][dataPointIndex] +
                        "</div>"
                    );
                },
            },
        };

        chartInferences = new ApexCharts(
            document.querySelector("#driveInferences"),
            inferencesOptions,
        );
        chartFPS = new ApexCharts(
            document.querySelector("#driveFPS"),
            fpsOptions,
        );

        chartInferences.render();
        chartFPS.render();

        // Adding event listeners
        lottieElement1.addEventListener("mouseenter", () =>
            playLottie(dotLottie1),
        );
        lottieElement1.addEventListener("mouseleave", () =>
            pauseLottie(dotLottie1),
        );

        lottieElement2.addEventListener("mouseenter", () =>
            playLottie(dotLottie2),
        );
        lottieElement2.addEventListener("mouseleave", () =>
            pauseLottie(dotLottie2),
        );

        lottieElement3.addEventListener("mouseenter", () =>
            playLottie(dotLottie3),
        );
        lottieElement3.addEventListener("mouseleave", () =>
            pauseLottie(dotLottie3),
        );

        if (dotLottie2) {
            playLottie(dotLottie2);
            setTimeout(() => {
                if (dotLottie2) {
                    pauseLottie(dotLottie2);
                }
            }, 2000);
        }

        return () => {
            lottieElement1.removeEventListener("mouseenter", () =>
                playLottie(dotLottie1),
            );
            lottieElement1.removeEventListener("mouseleave", () =>
                pauseLottie(dotLottie1),
            );

            lottieElement2.removeEventListener("mouseenter", () =>
                playLottie(dotLottie2),
            );
            lottieElement2.removeEventListener("mouseleave", () =>
                pauseLottie(dotLottie2),
            );

            lottieElement3.removeEventListener("mouseenter", () =>
                playLottie(dotLottie3),
            );
            lottieElement3.removeEventListener("mouseleave", () =>
                pauseLottie(dotLottie3),
            );
            pauseLottie(dotLottie1);
            pauseLottie(dotLottie2);
            pauseLottie(dotLottie3);
        };
    });

    function goToVideo() {
        const encodedPath = encodeURIComponent(drive.videourl);
        VideoURL.set(drive.videourl);
        OriginalVideoURL.set(drive.videourl);
        originalVideoURL.set(drive.videourl);
        push(`/video/${encodedPath}`);
    }

    function handleVideoHover(event) {
        const video = event.currentTarget;
        video.currentTime = 0; // Start from the beginning
        video.playbackRate = 2; // Slow down the playback
        video.play(); // Play the video
    }

    function handleVideoLeave(event) {
        const video = event.currentTarget;
        video.pause(); // Pause the video
        video.currentTime = 0; // Reset to the beginning
    }

    let show = false;
    let showBB = false;

    function handleBack(){
        push('/drivegallery')
    }
</script>

<ProtectedRoutes>
    <div class="flex justify-start mx-16 mt-2">
        <button class="backArrow" on:click={handleBack}><Icon path={mdiArrowLeftTop} size={32} /></button>
    </div>
    <div class="w-11/12 h-full mx-auto my-6">
        <h1 class="text-center text-4xl font-bold pb-4">Drive Dashboard</h1>
        <div class="flex flex-row justify-between">
            <div
                id="drive"
                class="drive-card flex lg:flex-row flex-col justify-between items-center"
            >
                <p class="text-xl text-center">Drive Length</p>
                <div class="text-3xl font-bold">{drive.length}</div>
            </div>
            <div
                id="frameCount"
                class="drive-card flex lg:flex-row flex-col justify-between items-center"
            >
                <p class="text-xl text-center">Frame Count</p>
                <div class="text-3xl font-bold">{drive.frame_count}</div>
            </div>
            <div
                id="Inferences"
                class="drive-card flex lg:flex-row flex-col justify-between items-center"
            >
                <p class="text-xl text-center">Inferences</p>
                <div class="text-3xl font-bold">{drive.inferences}</div>
            </div>
            <div
                id="FPS"
                class="drive-card flex lg:flex-row flex-col justify-between items-center"
            >
                <p class="text-xl text-center">FPS</p>
                <div class="text-3xl font-bold">{drive.FPS}</div>
            </div>
        </div>
        <div class="pt-10 grid grid-cols-2 gap-10">
            <div
                class="w-full h-60 bg-dark-hover rounded-2xl flex flex-col justify-center"
            >
                <h1 class="pl-12 text-3xl text-left">Drive FPS</h1>
                <div class="flex justify-center">
                    <div class="graph" id="driveFPS"></div>
                </div>
            </div>
            <div
                class="w-full h-60 bg-dark-hover rounded-2xl flex flex-col justify-center"
            >
                <h1 class="pl-12 text-3xl text-left">Drive Inferences</h1>
                <div class="flex justify-center">
                    <div class="graph" id="driveInferences"></div>
                </div>
            </div>
            <div
                class="w-full h-auto p-6 bg-dark-hover rounded-2xl flex flex-col gap-4"
            >
                <h1 class="text-3xl pb-4">Drive Video</h1>
                <div class="rounded-sm max-h-96">
                    <div class="object-contain w-full mx-auto h-full">
                        <video
                            class="rounded-3xl mx-auto"
                            src={drive.videourl}
                            alt="drive_frame_preview"
                            muted
                            preload="metadata"
                            on:mouseenter={handleVideoHover}
                            on:mouseleave={handleVideoLeave}
                        ></video>
                    </div>
                </div>
            </div>
            <!-- Control panel div -->
            <div
                class="w-full h-full bg-dark-hover rounded-2xl flex flex-col justify-center"
            >
                <div class="grid grid-cols-2 gap-6 place-content-center m-6">
                    <div class="control-center w-full h-auto">
                        <div class="h-full flex items-center">
                            <button
                                class="hoverPlay"
                                on:click={goToVideo}
                                on:focus={() => (show = !show)}
                            >
                                <Tooltip bottom bind:active={show}>
                                    <h1 class="text-xl">Play Video</h1>
                                    <Icon path={mdiPlay} size={72} />
                                    <span slot="tip">View video</span>
                                </Tooltip>
                            </button>
                        </div>
                    </div>
                    <div class="control-center w-full h-auto">
                        <div class="w-10/12 flex flex-col">
                            <a href="/pipe">
                                <h1 class="text-3xl">Piping</h1>
                                <div bind:this={lottieElement1} class="w-full">
                                    <DotLottieSvelte
                                        src="https://lottie.host/f0d46bc9-9504-414d-8909-bc4ebd9b3745/dIFAt1lMbR.json"
                                        loop={true}
                                        autoplay={false}
                                        dotLottieRefCallback={(ref) =>
                                            (dotLottie1 = ref)}
                                        autoResizeCanvas
                                    />
                                </div>
                            </a>
                        </div>
                    </div>
                    <div class="control-center w-full h-auto">
                        <div class="w-10/12 flex flex-col">
                            <h1 class="text-3xl">Weaver</h1>
                            <div bind:this={lottieElement2} class="w-full">
                                <DotLottieSvelte
                                    src="https://lottie.host/3c802195-f445-4f03-ba05-b24152f79226/WUP1NpZe2T.json"
                                    loop={true}
                                    autoplay={true}
                                    dotLottieRefCallback={(ref) =>
                                        (dotLottie2 = ref)}
                                    autoResizeCanvas
                                />
                            </div>
                        </div>
                    </div>
                    <div class="control-center w-full h-auto">
                        <div
                            class="w-10/12 flex flex-col"
                            on:focus={() => (showBB = !showBB)}
                        >
                            <Tooltip bottom bind:active={showBB}>
                                <!-- ADD 'a' tag to go to the blackbox feature -->
                                <h1 class="text-3xl">Blackbox</h1>
                                <div class="h-full flex justify-center">
                                    <div
                                        bind:this={lottieElement3}
                                        class="w-1/2 mx-auto my-auto"
                                    >
                                        <DotLottieSvelte
                                            src="https://lottie.host/3a913257-6101-499c-9905-2126141eca33/iE9rq5CLvE.json"
                                            loop={true}
                                            autoplay={false}
                                            dotLottieRefCallback={(ref) =>
                                                (dotLottie3 = ref)}
                                            autoResizeCanvas
                                        />
                                    </div>
                                </div>
                                <span slot="tip">Coming soon...</span>
                            </Tooltip>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</ProtectedRoutes>

<style>
    .backArrow:hover {
        transform: scale(1.2);
    }
    video {
        aspect-ratio: 16/9;
        height: 100%;
    }

    .control-center {
        border-radius: 15px;
        background-color: #002e4d;
        padding: 1rem;
        margin: 0 auto 0 0;
        display: flex;
        justify-content: center;
        justify-items: center;
    }

    .control-center:hover {
        transform: translateY(-10px);
    }

    .drive-card {
        width: 22%;
        padding: 12px;
        background-image: linear-gradient(90deg, #007acc, #002e4d);
        border-radius: 8px;
        transition: background-image 0.3s ease;
    }

    .drive-card:hover {
        background-image: linear-gradient(270deg, #007acc, #002e4d);
    }

    .drive-card:hover {
        transform: scale(1.15);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add shadow for depth */
    }

    .drive-card p {
        color: white;
        margin: 0;
    }

    .graph {
        height: 10rem;
        width: 80%;
    }

    .hoverPlay:hover {
        transform: scale(1.15);
    }
</style>
