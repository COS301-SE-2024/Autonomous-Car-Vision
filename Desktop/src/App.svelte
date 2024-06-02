<script>
  import Router from 'svelte-spa-router';
  import routes from './routes/routes';
  import './assets/global.css';
</script>

<style>
    @import 'tailwindcss/tailwind.css';
</style>

<div>
  <Router {routes} />
</div>
