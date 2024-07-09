<script>
    import { Button, Tooltip } from "svelte-materialify";
    // Exported Parameters
  
    export let Model = {
      mName: "",
      mDescription: "",
      mVersion: "",
      mSummary: "",
      mStatus: "",
      mProfileImg: "https://deep-image.ai/_next/static/media/app-info-generator.bf08e63e.webp",
      mImg: "",
    };

    // export let key;
</script>


  <div class="content">
      <div class="content__item">
        <span class="content__number">Version: {Model.mVersion}</span>
        <h3 class="content__title">{Model.mName}</h3>
        <h4 class="content__subtitle"> </h4>
        <div class="content__text">{Model.mSummary}</div>
      </div>
      <button class="content__close">
        <svg class="icon icon--longarrow">
          <use xlink:href="#icon-longarrow"></use>
        </svg>
      </button>
  </div>


<style>
     @import '../assets/base.css';
 </style>