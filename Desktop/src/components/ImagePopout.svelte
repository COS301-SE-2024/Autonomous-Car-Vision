<script>
import { createEventDispatcher } from 'svelte';

export let ImageUrl = ''

const dispatch = createEventDispatcher()

const ClickOutsite = dispatch('ImageUrl')

</script>

<div class="popout">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src={ImageUrl} alt="image.jpeg" />
</div>

<style>
.popout {
    background-color: rgba(0, 0, 0, 0.2);
    position: fixed;
    z-index: 25;
    width: 100vw;
    height: 100vh;
    margin: calc(5vw + 5vh);
}

.popout img {
    height: 60vh;
    width: auto;
}
</style>