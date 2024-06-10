<script>
    import {Button, TextField, Icon, MaterialApp} from "svelte-materialify";
    import {mdiEyeOff, mdiEye} from "@mdi/js";
    import axios from 'axios';
    import {push} from "svelte-spa-router";

    let nToken = '';
    let pToken = '';
    let step = 1;
    let sString = '';
    let show = false;
    let uid = 0;

    const onSubmitUsername = async () => {
        console.log("Username/Email Step");
        console.log(nToken);

        try {
            const response = await axios.post('http://localhost:8000/getSalt/', {
                "uemail": nToken,
            });
            uid = response.data.uid;
            sString = response.data.salt
            console.log(sString)
            step = 2;
        } catch (error) {
            console.error('Failed to retrieve salt and UID:', error);
        }
    };

    const onSubmitPassword = async () => {
        console.log("Password Step");
        console.log(pToken);


        try {
            const {hash} = await window.electronAPI.hashPasswordSalt(pToken, sString);

            const response = await axios.post('http://localhost:8000/signin/', {
                "uid": uid,
                "password": hash,
            });
            console.log(response);
            localStorage.setItem('uid', JSON.stringify(response.data.uid));
            push("/otp")
        } catch (error) {
            console.error('Login Failed:', error);
        }
    };
</script>

<div class="lg:w-4/12 w-6/12 mx-auto py-4 my-4">
    <MaterialApp>
        <div class="flex flex-row gap-2">
            <a
                    class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
                    href="#/login"
            >
                <Button class="text-primary-text-light bg-primary-green-light" depressed block>Log In</Button>
            </a>
            <a
                    class="w-full h-14 flex flex-col flex-wrap justify-center items-center"
                    href="#/signup"
            >
                <Button class="text-primary-text-light bg-gray-light" depressed block>Sign Up</Button>
            </a>
        </div>
        <div class="w-full p-4 border-2 rounded-md border-green-500 mt-2">
            <div class="text-left">
                <h1 class="text-2xl">Welcome back!</h1>
                <p>Please enter your information.</p>
            </div>
            {#if step === 1}
                <div id="form" class="flex flex-col gap-1 py-2">
                    <TextField bind:value={nToken} outlined>Username/Email</TextField>
                    <Button class="bg-primary-green-light" on:click={onSubmitUsername} rounded block>Next</Button>
                </div>
            {/if}
            {#if step === 2}
                <div id="form" class="flex flex-col gap-1 py-2">
                    <TextField bind:value={pToken} outlined type={show ? "text" : "password"}>
                        Password
                        <!-- svelte-ignore a11y-click-events-have-key-events -->
                        <div
                                slot="append"
                                on:click={() => {
                                show = !show;
                            }}
                        >
                            <Icon path={show ? mdiEyeOff : mdiEye}/>
                        </div>
                    </TextField>
                    <Button class="bg-primary-green-light" on:click={onSubmitPassword} rounded block>Log in</Button>
                </div>
            {/if}
        </div>
    </MaterialApp>
</div>
