// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';
import Help from './Help.svelte';

import OTP from "./OTP.svelte"
import AccountSettings from "./AccountSettings.svelte"
import Visualize from '../pages/Visualize.svelte'
import Gallery from '../pages/GallaryPage.svelte'
import ChangePassword from "../routes/ChangePassword.svelte"
import ModelPage from './Models.svelte'
import VideoPage from './video/[videoUrl]/+page.svelte'
import Drives from './drives/[videoUrl]/+page.svelte'
import DriveGallery from './DriveGallery.svelte'
import Join from './Join.svelte'
import NewTeam from './NewTeam.svelte'
import Invite from './Invite.svelte'
import Install from './Install.svelte'
import TeamView from './TeamView.svelte'
import TeamNetwork from './TeamNetwork.svelte'
import StartCarla from './StartCarla.svelte'
import Svelvet from './Svelvet.svelte'
import Tests from './Tests.svelte'

const routes = {
    '/': Home,
    '/login': LogIn,
    '/signup': SignUp,
    '/otp': OTP,
    '/gallery':Gallery,
    '/visualize': Visualize,
    '/models': ModelPage,
    '/accountsettings' : AccountSettings,
    '/changePassword': ChangePassword,
    '/video/:VideoUrl': VideoPage,
    '/help': Help,
    '/drive/:driveurl': Drives,
    '/drivegallery': DriveGallery,
    '/join': Join,
    '/newTeam': NewTeam,
    '/invite': Invite,
    '/install': Install,
    '/teamView': TeamView,
    '/teamNetwork': TeamNetwork,
    '/svelvet': Svelvet,
    '/startCarla': StartCarla,
    '/tests': Tests
};

export default routes;