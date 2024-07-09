<script>
    import ModelsCard from "../components/ModelsCard.svelte";
    import ModelsCardContent from '../components/ModelsCardContent.svelte';
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
        <svg class="hidden">
            <symbol id="icon-arrow" viewBox="0 0 24 24">
              <title>arrow</title>
              <polygon points="6.3,12.8 20.9,12.8 20.9,11.2 6.3,11.2 10.2,7.2 9,6 3.1,12 9,18 10.2,16.8 " />
            </symbol>
            <symbol id="icon-drop" viewBox="0 0 24 24">
              <title>drop</title>
              <path d="M12,21c-3.6,0-6.6-3-6.6-6.6C5.4,11,10.8,4,11.4,3.2C11.6,3.1,11.8,3,12,3s0.4,0.1,0.6,0.3c0.6,0.8,6.1,7.8,6.1,11.2C18.6,18.1,15.6,21,12,21zM12,4.8c-1.8,2.4-5.2,7.4-5.2,9.6c0,2.9,2.3,5.2,5.2,5.2s5.2-2.3,5.2-5.2C17.2,12.2,13.8,7.3,12,4.8z" />
              <path d="M12,18.2c-0.4,0-0.7-0.3-0.7-0.7s0.3-0.7,0.7-0.7c1.3,0,2.4-1.1,2.4-2.4c0-0.4,0.3-0.7,0.7-0.7c0.4,0,0.7,0.3,0.7,0.7C15.8,16.5,14.1,18.2,12,18.2z" />
            </symbol>
            <symbol id="icon-longarrow" viewBox="0 0 54 24">
              <title>longarrow</title>
              <path d="M.42 11.158L12.38.256c.333-.27.696-.322 1.09-.155.395.166.593.467.593.903v6.977h38.87c.29 0 .53.093.716.28.187.187.28.426.28.716v5.98c0 .29-.093.53-.28.716a.971.971 0 0 1-.716.28h-38.87v6.977c0 .416-.199.717-.592.903-.395.167-.759.104-1.09-.186L.42 12.62a1.018 1.018 0 0 1 0-1.462z" />
            </symbol>
            <symbol id="icon-navarrow" viewBox="0 0 408 408">
              <title>navarrow</title>
              <polygon fill="#fff" fill-rule="nonzero" points="204 0 168.3 35.7 311.1 178.5 0 178.5 0 229.5 311.1 229.5 168.3 372.3 204 408 408 204"></polygon>
            </symbol>
        </svg> 
      <div class="slideshow">
        <div class="slideshow__deco"></div>
          <!--import slides and content-->
          {#each Models as Model, key}
               <ModelsCard {Model} {key} />
               <ModelsCardContent {Model} {key} />
          {/each}

      </div>
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
    {/if}
</ProtectedRoutes>

<style>
  @import '../assets/base.css';
</style>
