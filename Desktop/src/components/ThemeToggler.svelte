<script>
  import { theme } from '../stores/themeStore.js';

  let currentTheme;
  $: {
    theme.subscribe(value => {
      currentTheme = value;
    });
  }

  function toggleTheme() {
    if (currentTheme === 'highVizLight') {
      theme.set('highVizDark');
    } else {
      theme.set('highVizLight');
    }
  }
</script>

<div class:light-theme={$theme === 'highVizLight'} class:dark-theme={$theme === 'highVizDark'}>
  <label class="toggler">
    <!-- Toggle Input -->
    <input
      type="checkbox"
      on:change={toggleTheme}
      class="toggle-input"
      aria-label="Theme toggle"
    />

    <!-- Knob that moves -->
    <span class="toggle-knob"></span>

    <!-- Sun Icon -->
    <svg
      class="icon sun-icon"
      xmlns="http://www.w3.org/2000/svg"
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round">
      <circle cx="12" cy="12" r="5" />
      <path
        d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
    </svg>

    <!-- Moon Icon -->
    <svg
      class="icon moon-icon"
      xmlns="http://www.w3.org/2000/svg"
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    </svg>
  </label>
</div>

<style>
  /* General styles */
  .light-theme, .dark-theme {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }

  .toggler {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 60px;
    height: 30px;
    background-color: var(--base-content);
    border-radius: 50px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  /* Sun and Moon icons */
  .icon {
    width: 20px;
    height: 20px;
    transition: opacity 0.3s ease;
  }

  .sun-icon {
    position: absolute;
    left: 5px;
    opacity: 1; /* Ensure the sun icon is visible initially */
  }

  .moon-icon {
    position: absolute;
    right: 5px;
    opacity: 0; /* Hide the moon icon initially */
  }

  /* Toggle input (invisible but functional) */
  .toggle-input {
    appearance: none;
    position: absolute;
    width: 100%;
    height: 100%;
    margin: 0;
    cursor: pointer;
    outline: none;
  }

  /* Toggle knob that moves with animation */
  .toggle-knob {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 26px;
    height: 26px;
    background-color: var(--base-100);
    border-radius: 50%;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Move the knob to the right when checked */
  .toggle-input:checked + .toggle-knob {
    transform: translateX(30px);
  }

  /* Hide the sun icon and show the moon icon when checked */
  .toggler input:checked ~ .sun-icon {
    opacity: 0;
  }

  .toggler input:checked ~ .moon-icon {
    opacity: 1;
  }

</style>
