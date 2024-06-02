// routes.js
import Home from './Home.svelte';
import LogIn from './LogIn.svelte';
import SignUp from './SignUp.svelte';
import GallaryPage from "../pages/GallaryPage.svelte"
import ViewVideoModal from "../components/ViewVideoModal.svelte"
import Upload from "./Upload.svelte"
import OTP from "./OTP.svelte"
import AccountSettings from "./AccountSettings.svelte"

const routes = {
    '/': GallaryPage,
    '/login': LogIn,
    '/signup': SignUp,
};

export default routes;