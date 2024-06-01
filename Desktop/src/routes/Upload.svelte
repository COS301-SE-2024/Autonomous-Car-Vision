<script>
    import Dropzone from "svelte-file-dropzone";
  
    let files = {
      accepted: [],
    };
  
    function handleFilesSelect(e) {
      const { acceptedFiles, fileRejections } = e.detail;
      files.accepted = [...files.accepted, ...acceptedFiles];
      
      // Alert for rejected files
      fileRejections.forEach(rejection => {
        alert(`File rejected: ${rejection.file.name}\nReason: ${rejection.errors[0].message}`);
      });
    }
  </script>
  
  <Dropzone 
    on:drop={handleFilesSelect}
    accept="video/*"
    maxSize={100 * 1024 * 1024}
    minSize={1 * 1024 * 1024}
  />
  <h2>Accepted Files</h2>
  <ol>
    {#each files.accepted as item}
      <li>{item.name}</li>
    {/each}
  </ol>