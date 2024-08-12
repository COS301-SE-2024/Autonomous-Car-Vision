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

    let driveData = {};

    let videoElement;
    let videoPath;
    let timestamps;
    let preprocessTimes;
    let inferenceTimes;
    let postprocessTimes;
    let totalTimes;
    let fpsValues;

    let chartData, chartFPS;
    let dotLottie1, dotLottie2, dotLottie3;
    let lottieElement1, lottieElement2, lottieElement3;

    function playLottie(lottie) {
        lottie?.play();
    }

    function pauseLottie(lottie) {
        lottie?.pause();
    }

    function calculateStatistics(driveData) {
        if (!driveData || !driveData.length || !driveData[0].data.length) {
            throw new Error("Invalid driveData format");
        }

        // Extract the data
        const data = driveData[0].data;

        // Calculate total frames
        const totalFrames = data.length;

        // Calculate total inference time and total FPS
        let totalInferenceTime = 0;
        let totalFps = 0;

        data.forEach((entry) => {
            totalInferenceTime += entry.inference_time;
            totalFps += entry.fps;
        });

        // Calculate averages
        const averageInferenceTime = totalInferenceTime / totalFrames;
        const averageFps = totalFps / totalFrames;

        drive.FPS = averageFps.toFixed(2) * totalFrames;
        drive.inferences = averageInferenceTime.toFixed(3);
        drive.frame_count = totalFrames;

        return {
            averageFps: averageFps.toFixed(2), // rounding to 2 decimal places
            averageInferenceTime: averageInferenceTime.toFixed(3), // rounding to 3 decimal places
            totalFrames,
        };
    }

    onMount(async () => {
        videoPath = $location.replace("/drive/", "");
        videoPath = decodeURIComponent(videoPath);
        console.log(videoPath);
        drive.videourl = videoPath;
        console.log(drive.videourl);
        videoElement.addEventListener("loadedmetadata", () => {
            drive.length = videoElement.duration;
            console.log("Video Length: ", drive.length, "seconds");
        });

        try {
            const driveDirectory =
                await window.electronAPI.getDrivesDirectory();
            driveData = await window.electronAPI.readDriveLog(driveDirectory);
            calculateStatistics(driveData);
            console.log(driveData);
            driveData = driveData[0].data.slice(1);
            console.log(driveData);

            timestamps = driveData.map((entry) => entry.timestamp);
            preprocessTimes = driveData.map((entry) => entry.preprocess_time);
            inferenceTimes = driveData.map((entry) => entry.inference_time);
            postprocessTimes = driveData.map((entry) => entry.postprocess_time);
            totalTimes = driveData.map((entry) => entry.total_time);
            fpsValues = driveData.map((entry) => entry.fps);
        } catch (error) {
            console.error(error);
        }

        const inferencesOptions = {
            series: [
                {
                    name: "Preprocess Time",
                    data: preprocessTimes,
                },
                {
                    name: "Inference Time",
                    data: inferenceTimes,
                },
                {
                    name: "Postprocess Time",
                    data: postprocessTimes,
                },
                {
                    name: "Total Time",
                    data: totalTimes,
                },
                {
                    name: "FPS",
                    data: fpsValues,
                },
            ],
            chart: {
                height: 240,
                type: "line",
                stacked: false,
                zoom: {
                    type: "x",
                    enabled: true,
                    autoScaleYaxis: true,
                },
                toolbar: {
                    autoSelected: "zoom",
                },
            },
            tooltip: {
                enabled: true,
            },
            dataLabels: {
                enabled: false,
            },
            stroke: {
                curve: "smooth",
            },
            yaxis: {
                labels: {
                    show: false,
                },
            },
            xaxis: {
                tooltip: {
                    enabled: true,
                },
                labels: {
                    show: false,
                },
                axisTicks: {
                    show: false,
                },
            },
        };

        chartData = new ApexCharts(
            document.querySelector("#driveData"),
            inferencesOptions,
        );

        chartData.render();

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

    function handleBack() {
        push("/drivegallery");
    }
</script>

<ProtectedRoutes>
    <div class="flex justify-start mx-16 mt-2">
        <button class="backArrow" on:click={handleBack}
            ><Icon path={mdiArrowLeft} size={32} /></button
        >
    </div>
    <div class="w-11/12 h-full mx-auto my-6">
        <div class="flex flex-row justify-between">
            <div
                id="drive"
                class="drive-card flex lg:flex-row flex-col justify-between items-center"
            >
                <p class="text-xl text-center">Length</p>
                <div class="text-3xl font-bold">{drive.length}s</div>
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
                <p class="text-xl text-center">Average Inference Time</p>
                <div class="text-3xl font-bold">{drive.inferences}s</div>
            </div>
            <div
                id="FPS"
                class="drive-card flex lg:flex-row flex-col justify-between items-center"
            >
                <p class="text-xl text-center">FPS</p>
                <div class="text-3xl font-bold">{drive.FPS}</div>
            </div>
        </div>
        <div class="pt-10 grid grid-cols-1 pb-10">
            <div
                class="w-full h-80 gradient-card rounded-2xl flex flex-col justify-evenly"
            >
                <h1 class="pl-12 text-3xl text-left">Drive Data</h1>
                <div class="flex justify-center">
                    <div class="graph" id="driveData"></div>
                </div>
            </div>
        </div>
        <div class="grid grid-cols-2 gap-10">
            <div
                class="w-full h-auto p-6 gradient-card rounded-2xl flex flex-col justify-center"
            >
                <div class="rounded-sm max-h-96 w-full">
                    <div class="object-contain w-full mx-auto h-full">
                        <video
                            bind:this={videoElement}
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
                class="w-full h-full gradient-card rounded-2xl flex flex-col justify-center"
            >
                <div class="grid grid-cols-2 gap-6 place-content-center m-6">
                    <div class="control-center w-full h-auto">
                        <div class="h-full flex items-center">
                            <h1 class="text-3xl">Play Video</h1>
                            <button class="hoverPlay" on:click={goToVideo}>
                                <Icon path={mdiPlay} size={72} />
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
    .gradient-card {
        background-image: linear-gradient(45deg, #007acc, #012a3b);
    }

    .backArrow:hover {
        transform: scale(1.2);
    }
    video {
        aspect-ratio: 16/9;
        height: 100%;
    }

    .control-center {
        border-radius: 15px;
        background-image: linear-gradient(270deg, #007acc, #002e4d);
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
        color: rgb(230, 0, 0);
    }

    .hoverPlay:hover {
        transform: scale(1.15);
    }
</style>
