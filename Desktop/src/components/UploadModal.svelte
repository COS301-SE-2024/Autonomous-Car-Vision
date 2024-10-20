<script>
    import Dropzone from "svelte-file-dropzone";
    import toast, { Toaster } from "svelte-french-toast";
    import { isUploadLoading } from "../stores/uploadLoading";
    import RingLoader from "./RingLoader.svelte";
    import { Button, Icon } from "svelte-materialify";
    import { mdiClose, mdiDeleteOutline, mdiUpload } from "@mdi/js";
    import { theme } from "../stores/themeStore";

    export let videoSource = "";
    export let showModal;

    let dialog;
    let filename = "";
    let file;

    function handleFilesSelect(e) {
        const { acceptedFiles, fileRejections } = e.detail;

        if (acceptedFiles.length > 0) {
            videoSource = URL.createObjectURL(acceptedFiles[0]);
            filename = acceptedFiles[0].name;
            file = acceptedFiles[0];
        }

        // Alert for rejected files
        fileRejections.forEach((rejection) => {
            alert(
                `File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`,
            );
        });
    }

    const saveVideo = async () => {
        if (!videoSource) {
            toast.error("Upload a video file to get started", {
                duration: 5000,
                position: "top-center",
            });
            return;
        }
        isUploadLoading.set(true);
        setInterval(async () => {
            isUploadLoading.set(false);
        }, 5000);

        let uid = window.electronAPI.getUid();
        let token = window.electronAPI.getToken();
        let sizeInBytes = file.size;

        // Convert size to MB and round to 2 decimal places
        let size = (sizeInBytes / (1024 * 1024)).toFixed(2);
        let aip = "";
        let aport = "";
        let command = "SEND";
        try {
            let response = await window.electronAPI.openFTP(
                uid,
                token,
                size,
                filename,
                file.path,
                command,
            );

            if (response.success) {
                aip = response.ip;
                aport = response.port;
                // You can now use response.ip and response.port as needed
            } else {
                console.error("Error:", response.error);
            }
        } catch (error) {
            console.error("Error calling openFTP:", error);
        }

        await window.electronAPI.uploadToAgent(
            aip,
            aport,
            file.path,
            uid,
            size,
            token,
            filename,
        );

        try {
            // Save the file using the main process
            videoSource = await window.electronAPI.saveFile(
                file.path,
                filename,
            );
            let record = {
                mname: filename,
                localurl: videoSource,
            };
            // Insert the record into the database
            const response1 = await window.electronAPI.insertData(record);

            // Select the record from the database
            const response2 = await window.electronAPI.selectData(filename);

            toast.success("Video uploaded successfully", {
                duration: 5000,
                position: "top-center",
            });

            // sleep for 5 seconds
            await new Promise((resolve) => setTimeout(resolve, 5000));

            if (response2.success) {
                const mid = response2.data.dataValues.mid;
                const uid = window.electronAPI.getUid();
                const token = window.electronAPI.getToken();

            } else {
                console.error(
                    "Failed to retrieve the record:",
                    response2.error,
                );
            }

            showModal = false;
            push("/gallery");
        } catch (error) {
            console.error("Error occurred:", error);
        }
    };

    function removeVideo() {
        videoSource = "";
        filename = "";
        file = null;
    }

    $: if (dialog && showModal) dialog.showModal();

    function clearVideoData() {
        videoSource = "";
        filename = "";
        file = null;
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
{#if $theme === "highVizLight"}
    <dialog
        bind:this={dialog}
        on:close={() => {
            showModal = false;
            clearVideoData();
        }}
        on:click|self={() => dialog.close()}
    >
        <div on:click|stopPropagation>
            <Toaster />
            <div class="relative -left-2 mb-2">
                <Button class="" icon on:click={() => dialog.close()}>
                    <Icon path={mdiClose} size={32} />
                </Button>
            </div>
            <div class="flex flex-col justify-center items-center">
                {#if videoSource}
                    <div class="flex flex-row w-full h-full">
                        <video src={videoSource} controls>
                            <track kind="captions" />
                        </video>
                    </div>
                {:else}
                    <Dropzone
                        on:drop={handleFilesSelect}
                        accept="video/*"
                        containerStyles="border-color: #8492a6; color: black;"
                        multiple={false}
                    />
                {/if}
                <div class="w-full flex justify-between items-center mt-4">
                    {#if videoSource}
                        <Button class="bg-red" rounded on:click={removeVideo}>
                            Remove <Icon path={mdiDeleteOutline} size={28} />
                        </Button>
                    {/if}
                    <span class="flex-grow"></span>
                    <Button
                        rounded
                        class="bg-dark-primary font-bold py-2 px-4 hover:bg-dark-secondary"
                        on:click={saveVideo}
                        >Save
                        <Icon path={mdiUpload} size={28} />
                    </Button>
                </div>
                {#if $isUploadLoading}
                    <div class="flex justify-center">
                        <RingLoader />
                    </div>
                {/if}
            </div>
        </div>
    </dialog>
{:else}
    <dialog
        class="bg-dark-background"
        bind:this={dialog}
        on:close={() => {
            showModal = false;
            clearVideoData();
        }}
        on:click|self={() => dialog.close()}
    >
        <div on:click|stopPropagation>
            <Toaster />
            <div class="relative -left-2 mb-2">
                <Button class="text-white" icon on:click={() => dialog.close()}>
                    <Icon path={mdiClose} size={32} />
                </Button>
            </div>
            <div class="flex flex-col justify-center items-center">
                {#if videoSource}
                    <div class="flex flex-row w-full h-full">
                        <video src={videoSource} controls>
                            <track kind="captions" />
                        </video>
                    </div>
                {:else}
                    <Dropzone
                        on:drop={handleFilesSelect}
                        accept="video/*"
                        containerStyles="border-color: #8492a6; color: white; background-color: #011C27;"
                        multiple={false}
                    />
                {/if}
                <div class="w-full flex justify-between items-center mt-4">
                    {#if videoSource}
                        <Button
                            class="bg-red text-white"
                            rounded
                            on:click={removeVideo}
                        >
                            Remove <Icon path={mdiDeleteOutline} size={28} />
                        </Button>
                    {/if}
                    <span class="flex-grow"></span>
                    <Button
                        rounded
                        class="bg-dark-primary text-white font-bold py-2 px-4 hover:bg-dark-secondary"
                        on:click={saveVideo}
                        >Save
                        <Icon path={mdiUpload} size={28} />
                    </Button>
                </div>
                {#if $isUploadLoading}
                    <div class="flex justify-center">
                        <RingLoader />
                    </div>
                {/if}
            </div>
        </div>
    </dialog>
{/if}

<style>
    video {
        object-fit: contain;
        aspect-ratio: 16/9;
        height: 100%;
        width: 100%;
    }

    dialog {
        width: 40em;
        border-radius: 0.8em;
        border: none;
        padding: 0;
    }

    dialog::backdrop {
        background: rgba(0, 0, 0, 0.3);
    }

    dialog > div {
        padding: 1em;
    }
    dialog[open] {
        position: absolute;
        top: 20%;
        left: 40%;
        animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes zoom {
        from {
            transform: scale(0.5);
        }
        to {
            transform: scale(1);
        }
    }
    dialog[open]::backdrop {
        animation: fade 0.2s ease-out;
    }
    @keyframes fade {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
</style>
