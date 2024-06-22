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


app = FastAPI()


@app.get("/")
def status():
    return {"status": "online"}

def getHardwareInfo():
    try:
        if shutil.which('nvidia-smi') is not None:
            result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            if "NVIDIA-SMI" in result.stdout:
                if shutil.which('nvcc') is not None:
                    result = subprocess.run(['nvcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                    if "release" in result.stdout:
                        return True
    except:
        pass

    return False


@app.get("/install")
async def install():
    async with httpx.AsyncClient() as client:
        load_dotenv()
        # encrypt my public ecd key
        init_elyptic = cerberus.elyptic(True)
        agent_public = init_elyptic['public']
        agent_private = init_elyptic['private']

        agent_rsa = cerberus.asymmetric()
        agent_rsa_public = agent_rsa['public']
        agent_rsa_private = agent_rsa['private']

        data_to_encrypt = {
            "aid": os.getenv("AID"),
            "ecd_key": agent_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8'),
            "rsa_key": agent_rsa_public.decode('utf-8')
        }
        print("JSON data for encryption:", data_to_encrypt)
        with open("./public_key.pem", "rb") as key_file:
            pem_content = key_file.read()
            print("Public key content:\n", pem_content.decode())  # Print the content of the PEM file
        encrypted_message = cerberus.encrypt_message(pem_content, data_to_encrypt)
        print("Encrypted message: ", encrypted_message)

        # Transmit the encrypted data
        response2 = await client.post('http://127.0.0.1:8006/test',
                                      json={"aid": os.getenv("AID"), "message": encrypted_message})
        if response2.status_code != 200:
            raise HTTPException(status_code=response2.status_code, detail="Error posting encrypted data")
        print("Response:", response2.json())
        # session = cerberus.get_session(agent_private,)
        server_ecdh = cerberus.decrypt_ecdh_key_with_rsa(agent_rsa_private, response2.json()['encrypted_ecdh'])
        print("server ecdh decoded", server_ecdh)
        server_ecdh2 = load_pem_public_key(server_ecdh.encode('utf-8'))
        
        with open('./.env', 'w') as f:
            f.write(f"SERVER_ECDH={server_ecdh2}")

        # TODO persist your own pem files and the server's ecdh key.
        # This simmulates message passing
        # session = cerberus.get_session(agent_private, server_ecdh2)
        # message = cerberus.elyptic_encryptor(session, "hello")
        # response3 = await client.post('http://127.0.0.1:8006/message',
        #                               json={"aid": response.json()['aid'], "message": message})
        # if response3.status_code != 200:
        #     raise HTTPException(status_code=response2.status_code, detail="Error posting encrypted data")
        # print("Response:", response3.json())
        # print(server_ecdh)
        return {'message': "success"}

def findOpenPort():
    port = 8002
    ip = "127.0.0.1"
    # ip = socket.gethostbyname(socket.gethostname())
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((ip, port))
            if result == 0:
                port += 1
            else:
                break
    return ip, port

def startFTP(ip, port, old_uid, old_size, old_token):
    def receive_until_null(conn):
        data = b''
        while True:
            byte = conn.recv(1)
            if byte == b'\0':
                break
            data += byte
        return data.decode()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Server started and listening on {ip}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                # Receive UID
                data = receive_until_null(conn)
                # make data json
                data = json.loads(data)
                print(f"DATA: {data}")
                
                uid = data.get("uid")
                mid = data.get["mid"]
                size = data['size']
                token = data['token']
                command = data['command']
                
                

                directory = f"./Download/{uid}/"
                os.makedirs(directory, exist_ok=True)
                print(f"Directory {directory} created to store information.")

                print(f'Connected by {addr}')

                if command == "SEND":
                    filename = receive_until_null(conn)
                    print(f"File name: {filename}")

                    if not filename:
                        break
                    filepath = os.path.join(directory, filename)

                    with open(filepath, 'wb') as f:
                        print(f"Receiving file {filename}...")
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
                    print(f"File {filename} received and saved to {filepath}")

                elif command == "RETR":
                    filename = receive_until_null(conn)
                    print(f"File name: {filename}")

                    if not filename:
                        break
                    filepath = os.path.join(directory, filename)

                    if os.path.exists(filepath):
                        with open(filepath, 'rb') as f:
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
    aid = body['aid']
    size = body['size']
    utoken = body['utoken']
    backgroundTasks.add_task(startFTP, ip, port, aid, size, utoken)
    return {"aip": ip, "aport": port}

@app.post("/process/")
async def process(request: Request):
    # gets the name from the request
    try:
        body = await request.json()
        uid = body['uid']
        mid = body['mid']
        token = body['token']

        # fetch the file url

        # process the file
        if(getHardwareInfo()):
            return JSONResponse(status_code=200, content={"message": "Success"})
        # subprocess.run(['makensis', './package/setup.nsi'])

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
    return {'message': "ill start listening thanks"}