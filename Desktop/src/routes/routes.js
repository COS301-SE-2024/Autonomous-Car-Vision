// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';
import Help from './Help.svelte';

import Upload from "./Upload.svelte"
import OTP from "./OTP.svelte"
import AccountSettings from "./AccountSettings.svelte"
import Visualize from '../pages/Visualize.svelte'
import Gallery from '../pages/GallaryPage.svelte'
import ChangePassword from "../routes/ChangePassword.svelte"
import ModelPage from './Models.svelte'
import VideoPage from './video/[videoUrl]/+page.svelte'
import Drives from './drives/[videoUrl]/+page.svelte'
import DriveGallery from './DriveGallery.svelte'
import ThreeJS from './ThreeJS.svelte'

const routes = {
    '/': Home,
    '/login': LogIn,
    '/signup': SignUp,
    '/otp': OTP,
    '/gallery':Gallery,
    '/visualize': Visualize,
    '/upload':Upload,
    '/models': ModelPage,
    '/accountsettings' : AccountSettings,
    '/changePassword': ChangePassword,
    '/video/:VideoUrl': VideoPage,
    '/help': Help,
    '/drive/:driveurl': Drives,
    '/drivegallery': DriveGallery,
    '/threejs': ThreeJS,
};

export default routes;