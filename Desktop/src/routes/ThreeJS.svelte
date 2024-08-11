<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { onMount } from "svelte";
    import * as THREE from "three";
    import { PLYLoader } from "three/examples/jsm/loaders/PLYLoader.js";
    import { PointerLockControls } from "three/examples/jsm/controls/PointerLockControls.js";

    let canvas;
    let camera, scene, renderer, controls;
    let keys = {};
    let mouseX = 0,
        mouseY = 0;
    let pitchObject, yawObject;

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

    function initializeScene() {
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
        loader.load("maps/combined_map.ply", (geometry) => {
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
        });

        // Add event listener to exit Pointer Lock on 'Escape' key
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                document.exitPointerLock();
            }
            keys[event.key] = true;
        });

        document.addEventListener("keyup", (event) => {
            keys[event.key] = false;
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

        // Handle yaw with 'Q' and 'E' keys
        function handleYaw() {
            const yawSpeed = 2;
            if (keys["q"]) yawObject.rotation.y -= yawSpeed; // Yaw left
            if (keys["e"]) yawObject.rotation.y += yawSpeed; // Yaw right
        }

        function animate() {
            requestAnimationFrame(animate);

            // Update camera movement based on keys
            const speed = 3;
            if (keys["w"]) camera.translateZ(-speed); // Move forward
            if (keys["s"]) camera.translateZ(speed); // Move backward
            if (keys["a"]) camera.translateX(-speed); // Move left
            if (keys["d"]) camera.translateX(speed); // Move right
            if (keys[" "]) camera.translateY(speed); // Move up
            if (keys["Shift"]) camera.translateY(-speed); // Move down

            // Apply yaw controls
            handleYaw();

            renderer.render(scene, camera);
        }

        animate();
    }

    onMount(() => {
        initializeScene();

        // Handle window resizing
        function onWindowResize() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            renderer.setSize(width, height);
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
        }

        window.addEventListener("resize", onWindowResize);
        onWindowResize();

        return () => {
            window.removeEventListener("resize", onWindowResize);
        };
    });
</script>

<ProtectedRoutes>
    <canvas bind:this={canvas} style="width: 100%; height: 100%;"></canvas>
</ProtectedRoutes>

<style>
    canvas {
        display: block;
        width: 100%;
        height: 100%;
    }
</style>
