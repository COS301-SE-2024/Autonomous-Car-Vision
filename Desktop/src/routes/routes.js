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
import ChangePassword from "../routes/ChangePassword.svelte"

const routes = {
    '/': ChangePassword,
    '/login': LogIn,
    '/signup': SignUp,
    '/otp': OTP,
    '/gallary':Gallary,
    '/upload':Upload,
    '/accountsettings' : AccountSettings
    // 'changePassword': ChangePassword
};

export default routes;