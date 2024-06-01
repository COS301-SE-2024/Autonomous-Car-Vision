// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';

const routes = {
    '/': Home,
    '/login': LogIn,
    '/signup': SignUp,
};

export default routes;