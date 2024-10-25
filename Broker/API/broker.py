import json

from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import subprocess

import charon
import media
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

HOST_IP = os.getenv("HOST_IP")


@app.get("/")
def status():
    return {"status": "online"}


@app.get("/simAgent")
def simAgent():
    response = charon.obol()
    print("result of obol: \n", response)
    return response


@app.post("/simHandshake")
async def simHandshake(request: Request):
    message = await request.json()
    print("Message: ---------> ", message)
    resp = media.registerAgent(json.dumps(message), message["aid"])
    print(resp)
    return resp


@app.post("/simStore")
async def simStore():
    print("Getting available agents")
    agents = media.get_avail_store_agents(10)
    print("avail agents: ", agents)
    avail = None
    for agent in agents:
        if await charon.ping(agent['aip'], agent['aport']):
            avail = agent
            break
    if avail is None:
        avail = {"aid": 28, "aport": 8001, "aip": HOST_IP}

    if not await charon.ping(avail["aip"], avail["aport"]):
        return {"status": "no agents available"}
    print(avail)
    return avail

@app.post("/process")
async def process(request: Request):
    message = await request.json()
    print("Message: ---------> ", message)

@app.get("/agent")
def agent():
    response = charon.obol()
    print("result of obol:\n", response)

    aid = response["aid"]
    public = response["public"]

    public = base64.b64encode(public).decode("utf-8")
    with open("./package/.env", "w") as f:
        f.write(f"AID={aid}\n")
        f.write(f"PUBLIC_TEST={public}\n")
        f.write(f"HOST_IP=206.189.188.197")

    subprocess.run(["makensis", "./package/setup.nsi"])

    filePath = "./package/MyFastAPIAppSetup.exe"
    return FileResponse(filePath, filename="AgentSetup.exe")

@app.get("/windows")
def windows():
    filepath = "./package/HighViz Setup 1.0.0.exe"
    return FileResponse(filepath, filename="HighViz.exe")

@app.get("/linux")
def linux():
    filepath = "./package/HighViz-1.0.0.AppImage"
    return FileResponse(filepath, filename="HighViz.AppImage")

@app.get("/requirements")
def requirements():
    filepath = "./package/requirements.txt"
    return FileResponse(filepath, filename="requirements.txt")

@app.get("/testVid")
def testVid():
    filepath = "./package/testVidCarla.mp4"
    return FileResponse(filepath, filename="testVidCarla.mp4")

@app.post("/test")
async def test(request: Request):
    message = await request.json()
    mresp = charon.asymmetric_decryption(message["aid"], message["message"])
    print(">>> Response from agent")
    print(mresp)
    charon.storeAgentECDH(mresp["aid"], mresp["public"]["ecd_key"])
    print(">>> Generating broker ecdh key")
    eresp = charon.generate_broker_ecdh_keys(message["aid"], mresp["public"]["rsa_key"])

    return {"encrypted_ecdh": eresp["ecdh_public_encrypted"]}


@app.post("/message")
async def test(request: Request):
    message = await request.json()
    print(message)
    keys = charon.getECDH(message["aid"])
    print(keys)
    server_ecdh = load_pem_private_key(keys["pem_priv"].encode("utf-8"), password=None)
    agent_ecdh = load_pem_public_key(keys["agent_pem_pub"].encode("utf-8"))
    sesion = charon.get_session(server_ecdh, agent_ecdh)
    decrypted_message = charon.elyptic_decryptor(sesion, message["message"])
    print(decrypted_message)
    return {"message": "success"}


@app.post("/handshake")
async def handshake(request: Request):
    message = await request.json()
    print(">>>Handshake initiated", message)
    keys = charon.getECDH(message["aid"])
    print(keys)
    server_ecdh = load_pem_private_key(keys["pem_priv"].encode("utf-8"), password=None)
    agent_ecdh = load_pem_public_key(keys["agent_pem_pub"].encode("utf-8"))
    sesion = charon.get_session(server_ecdh, agent_ecdh)
    decrypted_message = charon.elyptic_decryptor(sesion, message["message"])
    print(decrypted_message)
    resp = media.registerAgent(decrypted_message, message["aid"], message["corporation"])
    print(resp)
    return resp


@app.post("/brokerStore")
async def brokerStore(request: Request):
    message = await request.json()
    print(">>>BrokerStore initiated", message)
    print("Getting available agents")
    agents = media.get_avail_store_agents(message['size'], message['corporation'])
    print("avail agents: ", agents)
    avail = None
    for agent in agents:
        if await charon.ping(agent['aip'], agent['aport']):
            avail = agent
            break
    if avail is None:
        avail = {"aid": 1, "aport": 8001, "aip": "localhost", "corporation": "dev"}

    if not await charon.ping(avail["aip"], avail["aport"]):
        return {"status": "no agents available"}
    print("Agent: ", avail)
    keys = charon.getECDH(avail["aid"])
    print(keys)
    server_ecdh = load_pem_private_key(keys["pem_priv"].encode("utf-8"), password=None)
    agent_ecdh = load_pem_public_key(keys["agent_pem_pub"].encode("utf-8"))
    sesion = charon.get_session(server_ecdh, agent_ecdh)
    message_to_encrypt = {
        "aid": avail["aid"],
        "utoken": message["utoken"],
        "size": message["size"],
    }
    print("Message queued for encryption: ", message_to_encrypt)
    emessage = charon.elyptic_encryptor(sesion, json.dumps(message_to_encrypt))
    print("Encrypted message: ", emessage)
    tranmit = await charon.transmit(avail["aip"], avail["aport"], emessage)
    print("Transmission to agent: ", tranmit)
    return {"error": "Transmission to agent failed."} if not tranmit else tranmit
