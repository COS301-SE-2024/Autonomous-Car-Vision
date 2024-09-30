<script>
  import { theme } from "../stores/themeStore.js";

  let currentTheme;
  $: {
    theme.subscribe((value) => {
      currentTheme = value;
    });
  }

  function toggleTheme() {
    if (currentTheme === "highVizLight") {
      theme.set("highVizDark");
    } else {
      theme.set("highVizLight");
    }
  }
</script>

<div
  class:light-theme={$theme === "highVizLight"}
  class:dark-theme={$theme === "highVizDark"}
>
  <label class="toggler">
    <span class="mode-text">{$theme === "highVizLight" ? "Light" : "Dark"}</span
    >

    <!-- Slider Button -->
    <input
      type="checkbox"
      on:change={toggleTheme}
      class="slider-input"
      aria-label="Theme toggle"
    />

    <!-- Slider Knob -->
    {#if $theme === "highVizLight"}
      <span class="slider-knob-light"></span>
    {:else}
      <span class="slider-knob-dark"></span>
    {/if}
  </label>
</div>

<style>
  /* General layout */
  .light-theme,
  .dark-theme {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  /* Toggler container */
  .toggler {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 40px;
    cursor: pointer;
    background-color: var(--toggle-background, #ccc);
    border-radius: 20px;
    padding: 5px;
  }

  /* Mode Text (Light or Dark Mode) */
  .mode-text {
    font-size: 16px;
    color: var(--text-color, #333);
    text-align: center;
    margin-right: 10px;
    transition: color 0.3s ease;
  }

  /* Slider knob */
  .slider-knob-light {
    position: absolute;
    top: 5px;
    left: 5px;
    width: 30px;
    height: 30px;
    background-color: var(--base-100, #fff);
    border-radius: 50%;
  }

  .slider-knob-dark {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 30px;
    height: 30px;
    background-color: var(--base-100, #fff);
    border-radius: 50%;
  }

  /* Slider input (invisible but functional) */
  .slider-input {
    appearance: none;
    position: absolute;
    width: 100%;
    height: 100%;
    margin: 0;
    cursor: pointer;
    outline: none;
    z-index: 2; /* Make sure input is clickable */
  }

  /* Light Mode colors */
  .light-theme {
    --toggle-background: #eee;
    --base-100: #fff;
    --text-color: #000;
  }

  /* Dark Mode colors */
  .dark-theme {
    --toggle-background: #555;
    --base-100: #333;
    --text-color: #fff;
  }
</style>
