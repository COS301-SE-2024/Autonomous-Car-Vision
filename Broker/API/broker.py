import json

from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import subprocess
# import setup
import charon
import media
import base64

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
    
    public = base64.b64encode(public).decode('utf-8')

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


@app.post("/handshake")
async def handshake(request: Request):
    message = await request.json()
    print(">>>Handshake initiated", message)
    keys = charon.getECDH(message['aid'])
    print(keys)
    server_ecdh = load_pem_private_key(keys['pem_priv'].encode('utf-8'), password=None)
    agent_ecdh = load_pem_public_key(keys['agent_pem_pub'].encode('utf-8'))
    sesion = charon.get_session(server_ecdh, agent_ecdh)
    decrypted_message = charon.elyptic_decryptor(sesion, message['message'])
    print(decrypted_message)
    resp = media.registerAgent(decrypted_message, message['aid'])
    print(resp)
    return resp


@app.post("/brokerStore")
async def brokerStore(request: Request):
    # gets file size, mid, uid, token,
    message = await request.json()
    print(">>>BrokerStore initiated", message)
    # print("Getting available agents")
    # agents = media.get_avail_store_agents(message['size'])
    # print("avail agents: ", agents)
    avail = None
    # for agent in agents:
    #     if await charon.ping(agent['aip'], agent['aport']):
    #         avail = agent
    #         break
    if avail is None:
        avail = {'aid': 28, 'aport': 8001, 'aip': '127.0.0.1'}

    if not await charon.ping(avail['aip'], avail['aport']):
        return {'status': 'no agents available'}
    print("Agent: ", avail)
    keys = charon.getECDH(message['aid'])
    print(keys)
    server_ecdh = load_pem_private_key(keys['pem_priv'].encode('utf-8'), password=None)
    agent_ecdh = load_pem_public_key(keys['agent_pem_pub'].encode('utf-8'))
    sesion = charon.get_session(server_ecdh, agent_ecdh)
    message_to_encrypt = {
        'aid': avail['aid'],
        'utoken': message['utoken'],
        'size': message['size'],
    }
    print("Message queued for encryption: ", message_to_encrypt)
    emessage = charon.elyptic_encryptor(sesion, json.dumps(message_to_encrypt))
    print("Encrypted message: ", emessage)
    tranmit = await charon.transmit(avail['aip'], avail['aport'], emessage)
    return {"error": "Transmission to agent failed."} if not tranmit else tranmit
