<script>
    import { Icon, Button, Tooltip } from "svelte-materialify";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { mdiArrowLeft } from "@mdi/js";
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import * as THREE from "three";
    import { PLYLoader } from "three/examples/jsm/loaders/PLYLoader.js";
    import { PointerLockControls } from "three/examples/jsm/controls/PointerLockControls.js";
    import { outputPipe } from "../stores/store";

    // Components
    import ImagePopout from "../components/ImagePopout.svelte";

    let canvas1, canvas2;
    let camera1,
        camera2,
        scene1,
        scene2,
        renderer1,
        renderer2,
        controls1,
        controls2;
    let activeCanvas = null; // Track the active canvas
    let keys = {};
    let pitchObject1, yawObject1, pitchObject2, yawObject2;
    let showTooltip = false;

    function applyJetColormap(geometry) {
        const positions = geometry.attributes.position.array;
        const colors = new Float32Array(positions.length);

        let zMin = Infinity;
        let zMax = -Infinity;

        for (let i = 2; i < positions.length; i += 3) {
            const z = positions[i];
            if (z < zMin) zMin = z;
            if (z > zMax) zMax = z;
        }

        for (let i = 2; i < positions.length; i += 3) {
            const z = positions[i];
            const zNorm = (z - zMin) / (zMax - zMin);
            const color = new THREE.Color().setHSL(1.0 - zNorm, 1.0, 0.5);
            colors[i - 2] = color.r;
            colors[i - 1] = color.g;
            colors[i] = color.b;
        }

        geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
    }

    function initializeScene(
        canvas,
        scene,
        camera,
        renderer,
        controls,
        yawObject,
        pitchObject,
        plyFile,
    ) {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(
            60,
            window.innerWidth / window.innerHeight,
            0.1,
            1000,
        );

        renderer = new THREE.WebGLRenderer({ canvas });
        renderer.setSize(window.innerWidth, window.innerHeight);

        // Use PointerLockControls for camera rotation
        controls = new PointerLockControls(camera, renderer.domElement);
        const loader = new PLYLoader();
        loader.load(plyFile, (geometry) => {
            geometry.computeBoundingBox();
            applyJetColormap(geometry);

            const material = new THREE.PointsMaterial({
                size: 1,
                vertexColors: true,
            });
            const pointCloud = new THREE.Points(geometry, material);
            scene.add(pointCloud);

            const bbox = geometry.boundingBox;
            const center = bbox.getCenter(new THREE.Vector3());
            const size = bbox.getSize(new THREE.Vector3()).length();
            camera.position.set(center.x, center.y, center.z + size);
            camera.lookAt(center);

            // Initialize camera rotation and movement objects
            pitchObject = new THREE.Object3D();
            yawObject = new THREE.Object3D();
            pitchObject.add(camera);
            scene.add(pitchObject);

            // Set initial camera orientation
            pitchObject.rotation.x = -Math.PI / 6;

            animate();
        });

        // Add event listener to enable Pointer Lock on click
        canvas.addEventListener("click", () => {
            canvas.requestPointerLock();
            activeCanvas = canvas; // Set this canvas as active
        });

        // Mouse movement event
        document.addEventListener("mousemove", (event) => {
            if (document.pointerLockElement === canvas) {
                const movementX = event.movementX || 0;
                const movementY = event.movementY || 0;

                yawObject.rotation.y -= movementX * 0.002;
                pitchObject.rotation.x -= movementY * 0.002;

                // Constrain pitch rotation
                pitchObject.rotation.x = Math.max(
                    -Math.PI / 2,
                    Math.min(Math.PI / 2, pitchObject.rotation.x),
                );
            }
        });

        function animate() {
            requestAnimationFrame(animate);

            if (activeCanvas === canvas) {
                // Only move if this is the active canvas
                // Update camera movement based on keys
                const speed = 3;

                if (canvas === canvas1) {
                    if (keys["w"]) camera.translateZ(-speed); // Move forward
                    if (keys["s"]) camera.translateZ(speed); // Move backward
                    if (keys["a"]) camera.translateX(-speed); // Move left
                    if (keys["d"]) camera.translateX(speed); // Move right
                    if (keys["e"]) camera.translateY(speed); // Move up
                    if (keys["q"]) camera.translateY(-speed); // Move down
                } else if (canvas === canvas2) {
                    if (keys["i"]) camera.translateZ(-speed); // Move forward
                    if (keys["k"]) camera.translateZ(speed); // Move backward
                    if (keys["j"]) camera.translateX(-speed); // Move left
                    if (keys["l"]) camera.translateX(speed); // Move right
                    if (keys["o"]) camera.translateY(speed); // Move up
                    if (keys["u"]) camera.translateY(-speed); // Move down
                }
            }

            renderer.render(scene, camera);
        }

        animate();

        return { scene, camera, renderer, controls, yawObject, pitchObject };
    }

    onMount(() => {
        ({
            scene: scene1,
            camera: camera1,
            renderer: renderer1,
            controls: controls1,
            yawObject: yawObject1,
            pitchObject: pitchObject1,
            plyFile: String,
        } = initializeScene(
            canvas1,
            scene1,
            camera1,
            renderer1,
            controls1,
            yawObject1,
            pitchObject1,
            "testData/combined_map.ply"
        ));

        ({
            scene: scene2,
            camera: camera2,
            renderer: renderer2,
            controls: controls2,
            yawObject: yawObject2,
            pitchObject: pitchObject2,
            plyFile: String,
        } = initializeScene(
            canvas2,
            scene2,
            camera2,
            renderer2,
            controls2,
            yawObject2,
            pitchObject2,
            "testData/combined_map.ply"
        ));

        // Handle window resizing
        function onWindowResize() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            renderer1.setSize(width, height);
            renderer2.setSize(width, height);
            camera1.aspect = width / height;
            camera2.aspect = width / height;
            camera1.updateProjectionMatrix();
            camera2.updateProjectionMatrix();
        }

        window.addEventListener("resize", onWindowResize);
        onWindowResize();

        // Handle keydown and keyup events
        document.addEventListener("keydown", (event) => {
            keys[event.key] = true;
        });

        document.addEventListener("keyup", (event) => {
            keys[event.key] = false;
        });

        return () => {
            window.removeEventListener("resize", onWindowResize);
            document.removeEventListener("keydown");
            document.removeEventListener("keyup");
        };
    });

    const output = {
        original: "testData/frame_000300_raw.png",
        lidar: "testData/lidar_image.png",
        bb: "testData/bb_image.png",
        taggr: "testData/taggr_image.png",
        processed_image: "testData/processed_image.png",
    };

    function moveDown1() {
        canvas1.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function moveDown2() {
        canvas2.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function back() {
        push("/svelvet");
    }
</script>

<ProtectedRoutes>
    <div class="">
        <div class="w-full flex justify-start p-2">
            <Tooltip right bind:active={showTooltip}>
                <Button
                    class="text-white p-2"
                    icon
                    on:click={back}
                    on:mouseover={() => (showTooltip = !showTooltip)}
                >
                    <Icon path={mdiArrowLeft} size={32} />
                </Button>
                <span slot="tip">Back</span>
            </Tooltip>
        </div>
        <div class="flex flex-row justify-evenly gap-3 px-2">
            <div class="object-cover">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                <ImagePopout image={output.original} alt="Original Image" />
            </div>
            {#if $outputPipe[0] || $outputPipe[3]}
                <div class="object-cover">
                    <!-- svelte-ignore a11y-img-redundant-alt -->
                    <ImagePopout image={output.lidar} alt="Lidar Image" />
                </div>
            {/if}
            {#if $outputPipe[1] || $outputPipe[3]}
                <div class="object-cover">
                    <!-- svelte-ignore a11y-img-redundant-alt -->
                    <ImagePopout image={output.bb} alt="Bounding Box Image" />
                </div>
            {/if}
            {#if $outputPipe[2] || $outputPipe[3]}
                <div class="object-cover">
                    <!-- svelte-ignore a11y-img-redundant-alt -->
                    <ImagePopout image={output.taggr} alt="Taggr Image" />
                </div>
            {/if}
            <div class="object-cover">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                <ImagePopout
                    image={output.processed_image}
                    alt="Processed Image"
                />
            </div>
        </div>
        <div class="h-1/2">
            <div class="flex flex-row gap-2 overflow-x-auto py-3 w-full">
                <div class="relative left-10 top-6 h-0 w-0 text-white">
                    <h1 class="text-2xl">Controls</h1>
                    <div class="w-40">
                        <p>Forward: W</p>
                        <p>Right: D</p>
                        <p>Left: A</p>
                        <p>Back: S</p>
                        <p>Up: E</p>
                        <p>Down: Q</p>
                        <p>Press 'Esc' to leave</p>
                    </div>
                </div>
                <canvas bind:this={canvas1} on:click={moveDown1} on:keydown>
                </canvas>
                <div class="relative left-10 top-6 h-0 w-0 text-white">
                    <h1 class="text-2xl">Controls</h1>
                    <div class="w-40">
                        <p>Forward: I</p>
                        <p>Right: L</p>
                        <p>Left: J</p>
                        <p>Back: K</p>
                        <p>Up: O</p>
                        <p>Down: U</p>
                        <p>Press 'Esc' to leave</p>
                    </div>
                </div>
                <canvas class="pr-2" bind:this={canvas2} on:click={moveDown2} on:keydown
                ></canvas>
            </div>
        </div>
    </div>
</ProtectedRoutes>

<style>
    canvas {
        padding: 0rem;
        border-radius: 15px;
        border-color: white;
        width: 90% !important;
        height: 100% !important;
    }

    ::-webkit-scrollbar {
        display: none;
    }
</style>
