<script>
    import Dropzone from "svelte-file-dropzone";

    export let videoSource;
    let filename = "";

    function handleFilesSelect(e) {
        const {acceptedFiles, fileRejections} = e.detail;

        if (acceptedFiles.length > 0) {
            videoSource = URL.createObjectURL(acceptedFiles[0]);
            filename = acceptedFiles[0].name;
        }

        // Alert for rejected files
        fileRejections.forEach((rejection) => {
            alert(
                `File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`
            );
        });
    }

    const saveVideo = async () => {
        const fs = require('fs');
        const formData = new FormData();


        let record = {
            mname: filename,
            localurl: videoSource,
        }
        try {
            // Insert the record into the database
            const response1 = await window.electronAPI.insertData(record);
            console.log(response1);

            // Select the record from the database
            const response2 = await window.electronAPI.selectData(filename);
            console.log(response2);

            if (response2.success) {
                const mid = response2.data.mid;
                const uid = localStorage.getItem('uid');
                const token = localStorage.getItem('token');

                const uploadResponse = await window.electronAPI.uploadFile(file.path, mid, uid, token, filename);
                console.log(uploadResponse);

                if (uploadResponse.success) {
                    console.log("success upload")
                    const updateresp = await window.electronAPI.updateData(mid, {serverurl: uploadResponse.data.server_url});
                    console.log(updateresp);
                    if (updateresp.success){
                        console.log("all stages completed, file uploaded")

                    }else{
                        console.error('Upload failed:', updateresp.error);
                    }
                } else {
                    console.error('Upload failed:', uploadResponse.error);
                }
            } else {
                console.error('Failed to retrieve the record:', response2.error);
            }
        } catch (error) {
            console.error('Error occurred:', error);
        }


    }
</script>

<div class="flex flex-col items-center justify-center border-2 border-gray shadow-lg p-6 rounded-lg bg-gray-light max-w-lg mx-auto my-8 relative space-y-5">
    {#if videoSource === ""}
        <Dropzone
                on:drop={handleFilesSelect}
                accept="video/*"
                containerStyles="border-color: #8492a6; color: black"
                multiple={false}
        />
    {:else}
        <video class="video-preview w-full mt-4" src={videoSource} controls>
            <track kind="captions">
        </video>
    {/if}
    <div class="w-full flex items-center mt-4">
        <span class="flex-grow"></span>
        <button class="bg-blue text-white font-bold py-2 px-4 rounded hover:bg-gary-dark" on:click={saveVideo}>Save
        </button>
    </div>
</div>