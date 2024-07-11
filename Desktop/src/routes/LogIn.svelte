<script>
  import LoginForm from "../components/LoginForm.svelte";
</script>

<div class="login mx-auto h-screen lg:w-1/3 w-1/2">
  <LoginForm />
  <video autoplay muted loop class="bgVideo">
    <source
      src="https://media.istockphoto.com/id/1031773008/video/san-francisco-in-the-night.mp4?s=mp4-640x640-is&k=20&c=cLl3-sAt4GfapKQ7vmq1ujefFsUWXlJkLMVCq53Gyuc="
      type="video/mp4"
    />
  </video>
</div>

<style>
  .bgVideo {
    position: fixed;
    right: 0;
    bottom: 0;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
    z-index: 0;
  }
</style>
