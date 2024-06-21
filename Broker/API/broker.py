from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import subprocess
# import setup
import charon

app = FastAPI()


@app.get("/")
def status():
    return {"status": "online"}


@app.get("/agent")
def agent():
    # So Obol refers to the journey of a soul to the underworld.
    # A person is burried with a gold coin. The soul takes its gold coin, offers it to charon,
    # who then ferries the soul across the river Styx. In this case. It bundles the agent...
    response = charon.obol()
    print("result of obol:\n", response)
    # TODO agent packaging...
    # TODO part of agent packaging is to persist aid to an env and pem_pub to a .pem
    
    aid = response['aid']
    public = response['public']
    
    # make env file
    with open('./package/.env', 'w') as f:
        f.write(f"AID={aid}\n")
        f.write(f"PUBLIC={public}")
        
    subprocess.run(['makensis', './package/setup.nsi'])
    
    filePath = './package/MyFastAPIAppSetup.exe'
    return FileResponse(filePath,  filename='MyFastAPIAppSetup.exe')

@app.post("/test")
async def test(request: Request):
    message = await request.json()
    mresp = charon.asymmetric_decryption(message['aid'], message['message'])
    print(">>> Response from agent")
    print(mresp)
    charon.storeAgentECDH(mresp['aid'], mresp['public']['ecd_key'])
    print(">>> Generating broker ecdh key")
    eresp = charon.generate_broker_ecdh_keys(message['aid'], mresp['public']['rsa_key'])
    return {'encrypted_ecdh': eresp['ecdh_public_encrypted']}

@app.post("/message")
async def test(request: Request):
    message = await request.json()
    print(message)
    keys = charon.getECDH(message['aid'])
    print(keys)
    server_ecdh = load_pem_private_key(keys['pem_priv'].encode('utf-8'), password=None)
    agent_ecdh = load_pem_public_key(keys['agent_pem_pub'].encode('utf-8'))
    sesion = charon.get_session(server_ecdh, agent_ecdh)
    decrypted_message = charon.elyptic_decryptor(sesion, message['message'])
    print(decrypted_message)
    return {'message': 'success'}