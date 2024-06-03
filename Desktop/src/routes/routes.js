// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';

import GallaryPage from "../pages/GallaryPage.svelte"
import ViewVideoModal from "../components/ViewVideoModal.svelte"
import Upload from "./Upload.svelte"
import OTP from "./OTP.svelte"
import AccountSettings from "./AccountSettings.svelte"
import Gallary from '../pages/GallaryPage.svelte';

const routes = {
    '/': Home,
    '/login': LogIn,
    '/signup': SignUp,
    '/otp': OTP,
    '/gallary':Gallary,
    '/upload':Upload,
};

export default routes;