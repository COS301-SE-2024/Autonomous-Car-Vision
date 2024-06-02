// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';
import Models from './Models.svelte'

const routes = {
    '/': Home,
    '/login': LogIn,
    '/signup': SignUp,
    '/models': Models,
};

export default routes;