from fastapi import FastAPI, BackgroundTasks
import socket
import os
import requests
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import FastAPI, HTTPException, Request
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
import httpx
import cerberus
import socket
import os
import subprocess
import shutil
import json
from dotenv import load_dotenv
import base64
import netifaces
import select

load_dotenv()
app = FastAPI()

HOST_IP = os.getenv("HOST_IP")


@app.get("/")
def status():
    return {"status": "online"}


def getHardwareInfo():
    try:
        if shutil.which("nvidia-smi") is not None:
            result = subprocess.run(
                ["nvidia-smi"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            if "NVIDIA-SMI" in result.stdout:
                if shutil.which("nvcc") is not None:
                    result = subprocess.run(
                        ["nvcc", "--version"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=True,
                    )
                    if "release" in result.stdout:
                        return True
    except:
        pass
    return False


@app.on_event("startup")
async def startup_event():
    await install()


# TODO TEST
@app.get("/install")
async def install():
    async with httpx.AsyncClient() as client:
        init_elyptic = cerberus.elyptic(True)
        agent_public = init_elyptic["public"]
        agent_private = init_elyptic["private"]

        agent_rsa = cerberus.asymmetric()
        agent_rsa_public = agent_rsa["public"]
        agent_rsa_private = agent_rsa["private"]

        data_to_encrypt = {
            "aid": os.getenv("AID"),
            "ecd_key": agent_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode("utf-8"),
            "rsa_key": agent_rsa_public.decode("utf-8"),
        }
        print("JSON data for encryption:", data_to_encrypt)

        test = os.getenv("PUBLIC_TEST")
        test = base64.b64decode(test)

        encrypted_message = cerberus.encrypt_message(test, data_to_encrypt)
        print("Encrypted message: ", encrypted_message)

        response2 = await client.post(
            "http://" + HOST_IP + ":8006/test",
            json={"aid": os.getenv("AID"), "message": encrypted_message},
        )
        if response2.status_code != 200:
            raise HTTPException(
                status_code=response2.status_code, detail="Error posting encrypted data"
            )
        print("Response:", response2.json())
        server_ecdh = cerberus.decrypt_ecdh_key_with_rsa(
            agent_rsa_private, response2.json()["encrypted_ecdh"]
        )
        print("server ecdh decoded", server_ecdh)
        server_ecdh2 = load_pem_public_key(server_ecdh.encode("utf-8"))

        session = cerberus.get_session(agent_private, server_ecdh2)
        capacity = ""
        if os.getenv("AGENT_TYPE") == "S":
            capacity = "store"
        elif os.getenv("AGENT_TYPE") == "P": 
            capacity = "process"
        else:
            capacity = "dual"       
            
        message = cerberus.elyptic_encryptor(
            session,
            json.dumps(
                {
                    "aip": findOpenPort()[0], 
                    "aport": 8010,
                    "capacity": capacity,
                    "storage": 290.4,
                    "identifier": "ACDC",
                }
            ),
        )
        response3 = await client.post(
            "http://" + HOST_IP + ":8006/handshake",
            json={"aid": os.getenv("AID"), "corporation": os.getenv("CORPORATION_NAME"), "message": message},
        )
        if response3.status_code != 200:
            raise HTTPException(
                status_code=response2.status_code, detail="Error posting encrypted data"
            )
        print("Response:", response3.json())
        print(server_ecdh)
        return {"message": "success"}

@app.get("/findOpenPort")
def findOpenPort():
    port = 8002
    
    try:
        ip = requests.get('https://api.ipify.org').text.strip()
        print(f"Public IP address: {ip}")
    except Exception as e:
        print(f"Error getting public IP: {e}")
        ip = '0.0.0.0'
        print("Using placeholder IP: 0.0.0.0")
    
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result == 0:
                port += 1
            else:
                break
    
    return ip, port


def startFTP(ip, port, old_uid, old_size, old_token):
    def receive_until_null(conn):
        data = b""
        while True:
            byte = conn.recv(1)
            if byte == b"\0":
                break
            data += byte
        return data.decode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        s.setblocking(False)
        print(f"Server started and listening on {ip}:{port}")
        
        # Add timeout logic
        timeout = 10  # 10 seconds timeout
        ready = select.select([s], [], [], timeout)
        
        if not ready[0]:
            print(f"No connection received within {timeout} seconds. Closing the server.")
            return "Timeout: No connection received."

        conn, addr = s.accept()
        with conn:
            data = receive_until_null(conn)
            data = json.loads(data)
            print(f"DATA: {data}")

            uid = data["uid"]
            mid = data["mid"]
            size = data["size"]
            token = data["token"]
            command = data["command"]

            directory = f"./Download/{uid}/"
            os.makedirs(directory, exist_ok=True)
            print(f"Directory {directory} created to store information.")

            print(f"Connected by {addr}")

            if command == "SEND":
                filename = receive_until_null(conn).strip('"').strip("'")
                print(f"Received filename: '{filename}'")

                if not filename:
                    return "No filename received."
                filepath = os.path.join(directory, filename)

                with open(filepath, "wb") as f:
                    print(f"Receiving file {filename}...")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                    print(f"File {filename} received and saved to {filepath}")

            elif command == "RETR":
                filename = receive_until_null(conn).strip('"').strip("'")
                print(f"Received filename: '{filename}'")

                if not filename:
                    return "No filename received."
                filepath = os.path.join(directory, filename)

                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        print(f"Sending file {filename}...")
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            conn.sendall(data)
                        print(f"File {filename} sent successfully.")
                else:
                    print(f"File {filename} does not exist.")

    s.close()
    return "Operation completed successfully."


@app.post("/startupFTPListener/")
async def startupFTPListener(backgroundTasks: BackgroundTasks, request: Request):
    ip, port = findOpenPort()
    body = await request.json()
    print(f"Body: \n{body}")
    aid = os.getenv("AID")
    size = "STUMPED"
    utoken = "STUMPED"
    backgroundTasks.add_task(startFTP, ip, port, aid, size, utoken)
    return {"aip": ip, "aport": port, "aid": aid}


@app.post("/process/")
async def process(request: Request):
    try:
        body = await request.json()
        uid = body["uid"]
        mid = body["mid"]
        token = body["token"]
        if getHardwareInfo():
            return JSONResponse(status_code=200, content={"message": "Success"})
    except:
        return JSONResponse(status_code=400, content={"message": "Invalid request"})


def verifyOTP(otp):
    otp = "1234"
    if otp == "1234":
        return True
    else:
        return False


@app.post("/listen")
async def listen(request: Request):
    message = await request.json()
    print(message)
    return {"message": "ill start listening thanks"}
