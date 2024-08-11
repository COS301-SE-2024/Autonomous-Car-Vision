<script>
    import { Button, Icon  } from "svelte-materialify";
    import { mdiEyeOff, mdiEye } from "@mdi/js";

    let currentStep = 0;
    const steps = [
        "Step 1: Download the agent",
        "Step 2: Open the installer",
        "Step 3: Accept the license agreement",
        "Step 4: Choose the installation directory",
        "Step 5: Install the agent",
        "Step 6: Wait for the installation to complete",
        "Step 7: Finish and run the agent"
    ];

    function next() {
        if (currentStep < steps.length - 1) {
            currentStep += 1;
        } else {
            // Logic to move to the rest of the application can go here
            alert("Installation complete! Moving on to the rest of the application...");
        }
    }

    function back() {
        if (currentStep > 0) {
            currentStep -= 1;
        }
    }
</script>

<style>
    .slide {
        text-align: center;
        margin-top: 50px;
    }
    .controls {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .button {
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius:15px;
        color: var(--theme-dark-primary);
    }
    .container{
      background-image: linear-gradient(180deg,#181818, #001524 );
    }
</style>


<div class="lg:w-4/12 w-6/12 mx-auto py-14 mb-4">
    <div class="container text-white">
        <div class="slide">
            <h2 class="text-xl">{steps[currentStep]}</h2>
            <p class="p-2"> More information goes here... <br> and most probably images <br> but you get the point though....</p>
        </div>
        
        <div class="controls">
            <button class="button bg-theme-dark-primary text-theme-dark-lightText" on:click={back} disabled={currentStep === 0}>
                Back
            </button>
        
            {#if currentStep < steps.length - 1}
                <button class="button bg-theme-dark-primary text-theme-dark-lightText" on:click={next}>
                    Next
                </button>
            {:else}
                <button class="button bg-theme-dark-primary text-theme-dark-lightText" on:click={next}>
                   <!-- TODO: Just check that it doesn't lead to home but leads to the app -->
                    <a href="#/gallery"> 
                        Finish
                    </a>
                </button>
            {/if}
        </div>
    </div>
</div>  
