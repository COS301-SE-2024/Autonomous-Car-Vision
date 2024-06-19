// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';

import Upload from "./Upload.svelte"
import OTP from "./OTP.svelte"
import AccountSettings from "./AccountSettings.svelte"
import Gallary from '../pages/GallaryPage.svelte';
import ChangePassword from "../routes/ChangePassword.svelte"
import ModelPage from './Models.svelte'
import VideoPage from './Video.svelte'

const routes = {
    '/': LogIn,
    '/login': LogIn,
    '/signup': SignUp,
    '/otp': OTP,
    '/gallery':Gallary,
    '/upload':Upload,
    '/models': ModelPage,
    '/accountsettings' : AccountSettings,
    '/changePassword': ChangePassword,
    '/video' :VideoPage,
};

export default routes;