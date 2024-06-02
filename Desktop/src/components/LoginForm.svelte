<script>
    import { Button, TextField, Icon, MaterialApp } from "svelte-materialify";
    import { mdiEyeOff, mdiEye } from "@mdi/js";
    import axios from 'axios';

    let nToken = '';
    let pToken = ''

    const onSubmit = async () => {
        console.log("Login");
        console.log(nToken);
        console.log(pToken);

        try {
            // const response = await axios.post('http://localhost:8000/signin/', {
            //     "uname": nToken,
            //     ""
            // });
            // console.log('Login Successful:', response.data);\
            console.log('Hello')
        } catch (error) {
            console.error('Login Failed:', error);
        }
    };


    let show = false;
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
            <div id="form" class="flex flex-col gap-1 py-2">
                <!-- <label for="uName-Email">Username or Email</label> -->
                <TextField bind:value={nToken} outlined>Username/Email</TextField>
                <!-- <label for="uName-Email">Password</label> -->
                <TextField bind:value={pToken} outlined type={show ? "text" : "password"}>
                    Password
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <div
                        slot="append"
                        on:click={() => {
                            show = !show;
                        }}
                    >
                        <Icon path={show ? mdiEyeOff : mdiEye} />
                    </div>
                </TextField>
            </div>
            <Button class="bg-primary-green-light" on:click={onSubmit} rounded block
                >Log in</Button
            >
        </div>
    </MaterialApp>
</div>
