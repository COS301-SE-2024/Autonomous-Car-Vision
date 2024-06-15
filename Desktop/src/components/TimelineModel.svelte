<script>
  export let Model = {
    
    profileImage : '',
    modelName : '',
    lastUsedTimestamp : '',
    modelVersion : '',

  };

</script>

<div class="timeline-component">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src={Model.profileImage} alt="Profile Image" class="profile-image" />
    <div class="details">
      <span class="model-name">{Model.modelName}</span>
      <span class="timestamp">Last used: {Model.lastUsedTimestamp}</span>
    </div>
    <div class="version">
      v{Model.modelVersion}
    </div>
 
</div>