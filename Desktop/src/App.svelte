<script>
  import Router from "svelte-spa-router";
  import routes from "./routes/routes";

  window.electronAPI.getToken();
  let ttoken;
  if (window.electronAPI.getToken() != "") {
    ttoken = window.electronAPI.getToken();
  }

  console.log(window.electronAPI.getToken());
</script>

<div>
  <Router {routes} />
</div>
