<script>
    import {Drawer, ThemeToggle} from 'svelvet';
</script>

<div class="absolute top-0 left-0">
    <Drawer height={900} zoom={0.70}>
        <ThemeToggle main='light' alt='dark' slot='toggle'/>
    </Drawer>
</div>