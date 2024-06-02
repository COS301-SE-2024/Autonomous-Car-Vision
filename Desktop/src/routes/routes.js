// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';
import OTP from './OTP.svelte';
import Gallary from '../pages/GallaryPage.svelte';

const routes = {
    '/': Home,
    '/login': LogIn,
    '/signup': SignUp,
    '/otp': OTP,
    '/gallary':Gallary,
};

export default routes;