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
import Join from './Join.svelte'
import NewTeam from './NewTeam.svelte'
import Invite from './Invite.svelte'
import Install from './Install.svelte'
import Team from './Team.svelte'


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
    '/join': Join,
    '/newTeam': NewTeam,
    '/invite': Invite,
    '/install': Install,
    '/team': Team,
};

export default routes;