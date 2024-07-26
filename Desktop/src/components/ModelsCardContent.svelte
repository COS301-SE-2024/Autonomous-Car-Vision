<script>
    import { Button, Tooltip } from "svelte-materialify";
    // Exported Parameters
  
    export let Model = {
      mName: "",
      mDescription: "",
      mVersion: "",
      mSummary: "",
      mStatus: "",
      mProfileImg: "https://cdn.pixabay.com/photo/2024/03/11/19/15/ai-generated-8627457_640.png",
      mImg: "",
    };

    // export let key;
</script>


  <div class="content">
      <div class="content__item">
        <span class="content__number">Version: {Model.mVersion}</span>
        <h3 class="content__title">{Model.mName}</h3>
        <h4 class="content__subtitle"> {Model.mDescription}</h4>
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