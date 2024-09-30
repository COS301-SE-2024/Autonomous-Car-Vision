<script>
    import { Button, Icon  } from "svelte-materialify";
    import { mdiEyeOff, mdiEye } from "@mdi/js";
  import { push } from "svelte-spa-router";
  import {theme } from "../stores/themeStore";


    let currentStep = 0;
    const steps = [
        {
            step: "Step 1",
            context:"Download the agent" ,
            img: "./images/step1.png"
        },
        {
            step: "Step 2",
            context:"Open the installer" ,
            img: "./images/step2.png"
        },
        {
            step: "Step 3",
            context:"Choose your agent type" ,
            img: "./images/step3.png"
        },
        {
            step: "Step 4",
            context:"Choose the installation directory" ,
            img: "./images/step4.png"
        },
        {
            step: "Step 5",
            context:"Install the agent" ,
            img: "./images/step5.png"
        },
        {
            step: "Step 6",
            context:"Wait for the installation to complete" ,
            img: "./images/step6.png"
        },
        {
            step: "Step 7",
            context:"Finish and run the agent" ,
            img: "./images/HomeAnimation.gif"
        }
    ]; 

    function next() {
        if (currentStep < steps.length - 1) {
            currentStep += 1;
        } else {
            // Logic to move to the rest of the application can go here
            alert("Installation complete! Moving on to the rest of the application...");
            push("/gallery");
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
        align-content: center;
        justify-content: center;
        justify-items: center;
        align-items: center;
    }
    .controls {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .button {
        /* padding: 10px 20px; */
        font-size: 16px;
        cursor: pointer;
        border-radius:15px;
        color: var(--theme-dark-primary);
    }
    .containerClass{
      background-image: linear-gradient(180deg,#181818, #001524 );
      border-radius: 22px;
    }
    .containerClassLight{
      background-image: linear-gradient(180deg,#B6D9E8, #F8F8F8);
      border-radius: 22px;
    }

    .install-body {
        min-height: 80vh;
    }

    .image-style {
        min-height: 70vh;
    }
</style>


{#if $theme === 'highVizLight'}
<div class="lg:w-8/12 w-10/12 mx-auto py-4 mb-4 install-body">
    <div class="containerClassLight text-black items-center justify-center align-center">
        <div class="slide">
            <h2 class="text-xl">{steps[currentStep].step}</h2>
            <p class="p-2 text-lg text-bold">  {steps[currentStep].context}</p>
            <div class="flex justify-center"> 
                <img src={steps[currentStep].img} alt="{steps[currentStep].step}" class="self-center image-style" />
            </div>
        </div>
        
        <div class="controls p-4">
            <button class="button bg-theme-dark-primary text-theme-dark-lightText px-4 m-2" on:click={back} disabled={currentStep === 0}>
                Back
            </button>
        
            {#if currentStep < steps.length - 1}
                <button class="button bg-theme-dark-primary text-theme-dark-lightText px-4 m-2" on:click={next}>
                    Next
                </button>
            {:else}
                <button class="button bg-theme-dark-primary text-theme-dark-lightText px-4 m-2" on:click={next}>
                   <!-- TODO: Just check that it doesn't lead to home but leads to the app -->
                    <a href="#/gallery"> 
                        Finish
                    </a>
                </button>
            {/if}
        </div>
    </div>
</div>
{:else}
<div class="lg:w-8/12 w-10/12 mx-auto py-4 mb-4 install-body">
    <div class="containerClass text-white items-center justify-center align-center">
        <div class="slide">
            <h2 class="text-xl">{steps[currentStep].step}</h2>
            <p class="p text-lg text-bold-2">  {steps[currentStep].context}</p>
            <div class="flex justify-center"> 
                <img src={steps[currentStep].img} alt="{steps[currentStep].step}" class="self-center image-style" />
            </div>
        </div>
        
        <div class="controls p-4">
            <button class="button bg-theme-dark-primary text-theme-dark-lightText px-4 m-2" on:click={back} disabled={currentStep === 0}>
                Back
            </button>
        
            {#if currentStep < steps.length - 1}
                <button class="button bg-theme-dark-primary text-theme-dark-lightText px-4 m-2" on:click={next}>
                    Next
                </button>
            {:else}
                <button class="button bg-theme-dark-primary text-theme-dark-lightText px-4 m-2" on:click={next}>
                   <!-- TODO: Just check that it doesn't lead to home but leads to the app -->
                    <a href="#/gallery"> 
                        Finish
                    </a>
                </button>
            {/if}
        </div>
    </div>
</div>

{/if}
