<script>
  import Router from 'svelte-spa-router';
  import routes from './routes/routes';
</script>

<div>
  <Router {routes} />
  <!-- <LoginForm />
  
  <button on:click={() => navigate('/signin')}>Sign In</button>
  <button on:click={() => navigate('/signup')}>Sign Up</button> -->
</div>
