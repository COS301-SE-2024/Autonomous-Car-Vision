<script>
    import { Icon } from 'svelte-materialify';
    import { mdiClose } from '@mdi/js';


    export let image;
    export let alt;

    let modalVisible = false;
    let modalImgSrc = "";
    let modalCaption = "";

    function imgClick(event) {
        modalVisible = true;
        modalImgSrc = event.target.src;
        modalCaption = event.target.alt;
    }

    function spanClick() {
        modalVisible = false;
    }
</script>

<img
    class="mainImage"
    on:click={imgClick}
    on:keydown
    src={image}
    {alt}
    style="width:100%;"
/>

<!-- The Modal -->
{#if modalVisible}
    <div id="myModal" on:click={spanClick} on:keydown class="modal">
        <span class="close">
            <Icon path={mdiClose} size={32} on:click={spanClick} on:keydown />
        </span>
        <img class="modal-content" src={modalImgSrc} alt={modalCaption} />
        <div id="caption">{modalCaption}</div>
    </div>
{/if}

<style>
    .mainImage:hover {
        cursor: pointer;
        transform: scale(1.1);
    }

    /* The Modal (background) */
    .modal {
        display: block;
        position: fixed;
        z-index: 1;
        padding-top: 100px;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.9);
    }

    /* Modal Content (image) */
    .modal-content {
        margin: auto;
        display: block;
        width: 80%;
        max-width: 800px;
    }

    /* Caption of Modal Image */
    #caption {
        margin: auto;
        display: block;
        width: 80%;
        max-width: 700px;
        text-align: center;
        color: #ccc;
        padding: 10px 0;
        height: 150px;
    }

    /* Add Animation */
    .modal-content,
    #caption {
        animation-name: zoom;
        animation-duration: 0.6s;
    }

    @keyframes zoom {
        from {
            transform: scale(0);
        }
        to {
            transform: scale(1);
        }
    }

    /* The Close Button */
    .close {
        position: absolute;
        top: 15px;
        right: 35px;
        color: #f1f1f1;
        font-size: 40px;
        font-weight: bold;
        transition: 0.3s;
    }

    .close:hover,
    .close:focus {
        color: #bbb;
        text-decoration: none;
        cursor: pointer;
    }

    /* 100% Image Width on Smaller Screens */
    @media only screen and (max-width: 700px) {
        .modal-content {
            width: 100%;
        }
    }
</style>
