<script>
  import { Node, Anchor, Edge, generateInput, generateOutput } from "svelvet";

  export let identifier = "";
  export let connectors = [];
  export let position = { x: 0, y: 0 };
  export let label = "Output";
  export let bgColor = "lightblue";

  // To select an image to process
  let fileinput;

  /**
   * @type {InputStructure}
   */
  let fileUpload = {
    image: "",
  };

  const onFileSelected = (e) => {
    let image = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = (e) => {
      fileUpload.image = e.target.result;
      inputs = generateInput(fileUpload);
      output = generateOutput(inputs, processor);
    };
  };

  /**
   * @typedef {Object} InputStructure
   * @property {string} image
   */

  // Create initial values for your parameters
  /**
   * @type {InputStructure}
   */
  const initialData = {
    image: "https://media1.tenor.com/m/a0IapXcGUMYAAAAC/wheee-rally-car.gif",
  };

  // Specify processor function
  /**
   * @param {InputStructure} inputs
   * @returns {number}
   */
  const processor = (inputs) => {
    return inputs.image; // Show Image and return string image to processorNode
  };

  let inputs = generateInput(initialData);
  let output = generateOutput(inputs, processor);

  const key = Object.entries($inputs)[0][0];
</script>

<Node
  {position}
  id={identifier}
  connections={connectors}
  width={400}
  height={400}
  useDefaults
  {label}
  {bgColor}
>
  <div class="node">
    <div class="body">
      <div class="header w-full h-full text-center flex justify-center align-center" >
        <h1 class="text-3xl font-bold">{label}</h1>
      </div>
      <!-- <div class="showImage">
        {#if $inputs.image} -->
          <!-- <img src={$output} alt="ImageUploaded" /> -->
        <!-- {:else} -->
          <!-- <img
            src="https://media1.tenor.com/m/a0IapXcGUMYAAAAC/wheee-rally-car.gif"
            alt="inputImage"
          /> -->
        <!-- {/if} -->
        <!-- <img
          class="upload"
          src="https://static.thenounproject.com/png/625182-200.png"
          alt=""
          on:click={() => {
            fileinput.click();
          }}
          on:keydown
        /> -->
        <!-- <div
          class="chan"
          on:keydown
          on:click={() => {
            fileinput.click();
          }}
        >
          Choose Image
        </div>
        <input
          style="display:none"
          type="file"
          accept=".jpg, .jpeg, .png"
          on:change={(e) => onFileSelected(e)}
          bind:this={fileinput}
        /> -->
      <!-- </div> -->
    </div>
    <!-- <div class="input-anchors">
      <Anchor bgColor="green" {key} inputsStore={inputs} input />
    </div> -->
    <div class="output">
      <div class="output-anchors">
        <Anchor
          dynamic
          direction="east"
          id={identifier}
          bgColor="red"
          outputStore={output}
          output
        >
          <Edge slot="edge" color="red" 
          />
          <!-- label={$output}  -->
        </Anchor>
      </div>
    </div>
  </div>
</Node>

<style>
  .node {
    width: fit-content;
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .body {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    align-content: center;
    height: 100%;
  }

  .showImage {
    width: 80%;
    height: 80%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .upload {
    display: flex;
    height: 50px;
    width: 50px;
    cursor: pointer;
  }

  .input-anchors {
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 10px;
    top: 50%;
    left: 0px;
  }

  .output-anchors {
    position: absolute;
    right: 0px;
    bottom: 50%;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
</style>
