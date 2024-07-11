<script>
    import SignUpForm from "../components/SignUpForm.svelte";
</script>

<div class="signUp mx-auto h-screen lg:w-1/3 w-1/2">
    <SignUpForm />
    <video autoplay muted loop class="bgVideo">
        <source
            src="https://media.istockphoto.com/id/1495784351/video/japan-car-driving-video-june-2023.mp4?s=mp4-640x640-is&k=20&c=92_SQDV9QV3kKQrbIY7laxqt_dT6GloIn6NNyGZmJcw="
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
