<script>
    import ModelsCard from "../components/ModelsCard.svelte";
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { isLoading } from "../stores/loading";
    import Spinner from "../components/Spinner.svelte";
    import { onMount } from "svelte";

    let Models = [];

    onMount(async () => {

     //try {
    //   await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/imagesloaded.pkgd.min.js');
    //   await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/charming.min.js');
    //   await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/TweenMax.min.js');
    //   await loadScript('/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/demo.js');
    //   console.log('All scripts loaded successfully');
    // } catch (error) {
    //   console.error(error);
    // }

    const scripts = [
      '/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/imagesloaded.pkgd.min.js',
      '/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/charming.min.js',
      '/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/TweenMax.min.js',
      '/home/kea_mothapo/Desktop/ACV_Project/Autonomous-Car-Vision/Desktop/src/routes/modelsJS/demo.js'
    ];

    scripts.forEach(src => {
      const script = document.createElement('script');
      script.src = src;
      script.async = true;
      document.body.appendChild(script);
    });

    document.documentElement.className = 'js';
    const supportsCssVars = () => {
      const style = document.createElement('style');
      style.innerHTML = 'root: { --tmp-var: bold; }';
      document.head.appendChild(style);
      const supports = !!(window.CSS && window.CSS.supports && window.CSS.supports('font-weight', 'var(--tmp-var)'));
      style.parentNode.removeChild(style);
      return supports;
    };
    if (!supportsCssVars()) {
      alert('Please view this demo in a modern browser that supports CSS Variables.');
    }

        isLoading.set(true);
        try {
            const result = await window.electronAPI.getAIModels();
            if (result.success) {
                Models = result.data.map(model => ({
                    mName: model.model_name,
                    mDescription: model.model_summary,
                    mVersion: model.model_version,
                    mSummary: model.model_description,
                    mStatus: "green", // Assuming a default status; you can adjust this as needed
                    mProfileImg: model.model_profileimg,
                    mImg: model.model_img,
                }));
            } else {
                console.error('Failed to fetch AI models:', result.error);
            }
        } catch (error) {
            console.error("Failed to fetch data", error);
        } finally {
            isLoading.set(false);
        }
    });

    function handleSearch(event) {
    searchQuery = event.target.value;
    filteredItems = videoURLs.filter(item => {
      const searchRegex = new RegExp(searchQuery, 'i');

      if (filterCategory === 'Name') {
        return searchRegex.test(videoNames[item]);
      } else if (filterCategory === 'Date') {
        return searchRegex.test(item.date);
      } else if (filterCategory === 'Model Name') {
        return searchRegex.test(item.modelName);
      }
      return true;
    });
  }

  function handleFilterChange(event) {
    filterCategory = event.target.value;
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error(`Failed to load script ${src}`));
      document.head.appendChild(script);
    });
  }

 

</script>

<ProtectedRoutes>
    {#if $isLoading}
        <div class="flex justify-center">
            <Spinner />
        </div>
    {:else}
    <div class="flex justify-center items-center w-full mb-4 p-4 "> <!--TODO: style the searchbar -->
        <input
          type="text"
          placeholder="Search..."
          on:input{handleSearch}
          class="bg-theme-dark-white rounded-lg border-2 border-theme-dark-secondary p-2 w-5/6 border-solid text-lg" 
          />
        <!-- TODO: style filter bar-->
        <select class="bg-theme-dark-secondary  rounded-lg ml-2 p-2  text-lg" 
          on:change={handleFilterChange}
          placeholder="Filter...">
            <option value="All">Filter...</option>
            <option value="Name">Name</option>
            <option value="Date">Date</option>
            <option value="Model Name">Model Name</option>
        </select>
      </div>
      <div>
        <div class="slideshow relative overflow-hidden m-0 h-screen w-full grid"> 
             <div class="slideshow__deco"></div>
             <!-- <ModelsCard /> -->
            {#each Models as Model, key}
                <ModelsCard {Model} {key} />
            {/each}
            <button class="nav nav--prev">
                <svg class="icon icon--navarrow-prev">
                    <use xlink:href="#icon-navarrow"></use>
                </svg>
            </button>
            <button class="nav nav--next">
                <svg class="icon icon--navarrow-next">
                    <use xlink:href="#icon-navarrow"></use>
                </svg>
            </button>
        </div>
    </div>
    {/if}
</ProtectedRoutes>

<style>

    :global(article), :global(aside), :global(details), :global(figcaption), :global(figure), :global(footer), :global(header), :global(hgroup), :global(main), :global(nav), :global(section), :global(summary) { display: block; }
  :global(audio), :global(canvas), :global(video) { display: inline-block; }
  :global(audio:not([controls])) { display: none; height: 0; }
  :global([hidden]) { display: none; }
  :global(html) { font-family: sans-serif; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; }
  :global(body) { margin: 0; }
  :global(a:focus) { outline: thin dotted; }
  :global(a:active), :global(a:hover) { outline: 0; }
  :global(h1) { font-size: 2em; margin: 0.67em 0; }
  :global(abbr[title]) { border-bottom: 1px dotted; }
  :global(b), :global(strong) { font-weight: bold; }
  :global(dfn) { font-style: italic; }
  :global(hr) { -moz-box-sizing: content-box; box-sizing: content-box; height: 0; }
  :global(mark) { background: #ff0; color: #000; }
  :global(code), :global(kbd), :global(pre), :global(samp) { font-family: monospace, serif; font-size: 1em; }
  :global(pre) { white-space: pre-wrap; }
  :global(q) { quotes: "\201C" "\201D" "\2018" "\2019"; }
  :global(small) { font-size: 80%; }
  :global(sub), :global(sup) { font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; }
  :global(sup) { top: -0.5em; }
  :global(sub) { bottom: -0.25em; }
  :global(img) { border: 0; }
  :global(svg:not(:root)) { overflow: hidden; }
  :global(figure) { margin: 0; }
  :global(fieldset) { border: 1px solid #c0c0c0; margin: 0 2px; padding: 0.35em 0.625em 0.75em; }
  :global(legend) { border: 0; padding: 0; }
  :global(button), :global(input), :global(select), :global(textarea) { font-family: inherit; font-size: 100%; margin: 0; }
  :global(button), :global(input) { line-height: normal; }
  :global(button), :global(select) { text-transform: none; }
  :global(button), :global(html input[type="button"]), :global(input[type="reset"]), :global(input[type="submit"]) { -webkit-appearance: button; cursor: pointer; }
  :global(button[disabled]), :global(html input[disabled]) { cursor: default; }
  :global(input[type="checkbox"]), :global(input[type="radio"]) { box-sizing: border-box; padding: 0; }
  :global(input[type="search"]) { -webkit-appearance: textfield; appearance: textfield; -moz-box-sizing: content-box; -webkit-box-sizing: content-box; box-sizing: content-box; }
  :global(input[type="search"]::-webkit-search-cancel-button), :global(input[type="search"]::-webkit-search-decoration) { -webkit-appearance: none; }
  :global(button::-moz-focus-inner), :global(input::-moz-focus-inner) { border: 0; padding: 0; }
  :global(textarea) { overflow: auto; vertical-align: top; }
  :global(table) { border-collapse: collapse; border-spacing: 0; }
  :global(*), :global(*::after), :global(*::before) { box-sizing: border-box; }
    .slideshow{
    overflow:hidden;
    display: grid;
	grid-template-columns: 33% 33% 33%;
	grid-column-gap: 0.5%;
	grid-template-rows: 100%;
	grid-template-areas: '... slide ...';
    }

    .slideshow__deco {
	grid-area: slide;
	background: var(--color-deco);
	width: 100%;
	height: 80%;
	align-self: center;
	position: relative;
	margin: -40px 0 0 0;
	right: -20px;
}


.nav {
	position: absolute;
	background: none;
	width: 3rem;
	height: 3rem;
	z-index: 1000;
	border: 0;
	padding: 0;
	margin: 0;
	pointer-events: none;
	transition: transform 0.8s, opacity 0.8s;
	transition-timing-function: cubic-bezier(0.7,0,0.3,1);
}

.nav--next {
	bottom: 1rem;
	right: 1rem;
}

.icon--navarrow-next {
	transform: rotate(45deg);
}

.nav--prev {
	top: 1rem;
	left: 1rem;
}

.icon--navarrow-prev {
	transform: rotate(-135deg);
}

.slideshow--previewopen .nav {
	opacity: 0;
	transition-duration: 0.4s;
}

.slideshow--previewopen .nav--next {
	transform: translate3d(100%, 100%, 0);
}

.slideshow--previewopen .nav--prev {
	transform: translate3d(-100%, -100%, 0);
}

@media screen and (min-width: 53em) {
  .slideshow {
		height: 100vh;
		grid-template-columns: 27% 27% 27%;
		grid-column-gap: 9.5%;
	}
}
</style>
