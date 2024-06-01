<script>
  import Dropzone from "svelte-file-dropzone";
  import FileItem from "../components/FileItem.svelte";

  let files = {
    accepted: [],
  };

  function handleFilesSelect(e) {
    const { acceptedFiles, fileRejections } = e.detail;
    files.accepted = [...files.accepted, ...acceptedFiles];

    // Alert for rejected files
    fileRejections.forEach((rejection) => {
      alert(
        `File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`
      );
    });
  }

  function removeFile(file) {
    files.accepted = files.accepted.filter((f) => f !== file);
  }
</script>

<div class="flex flex-col items-center">
  <Dropzone
    on:drop={handleFilesSelect}
    accept="video/*"
    maxSize={100 * 1024 * 1024}
    minSize={1 * 1024 * 1024}
    containerStyles="border-color: #8492a6; color: black"
  />
  <h2>Files to be uploaded</h2>
  <ol>
    {#each files.accepted as item}
      <FileItem file={item} onRemove={removeFile} />
    {/each}
  </ol>
</div>
