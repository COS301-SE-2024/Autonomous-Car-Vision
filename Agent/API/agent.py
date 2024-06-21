from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import FastAPI, HTTPException, BackgroundTasks
import httpx
import cerberus
import socket
import os

app = FastAPI()


@app.get("/")
def status():
    return {"status": "online"}


@app.get("/install")
async def install():
    async with httpx.AsyncClient() as client:
        # get my agent details
        response = await client.get('http://127.0.0.1:8006/agent')
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching external data")
        print("Response:", response.json())

        # encrypt my public ecd key
        init_elyptic = cerberus.elyptic(True)
        agent_public = init_elyptic['public']
        agent_private = init_elyptic['private']

        agent_rsa = cerberus.asymmetric()
        agent_rsa_public = agent_rsa['public']
        agent_rsa_private = agent_rsa['private']

        data_to_encrypt = {
            "aid": response.json()['aid'],
            "ecd_key": agent_public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8'),
            "rsa_key": agent_rsa_public.decode('utf-8')
        }
        print("JSON data for encryption:", data_to_encrypt)

        encrypted_message = cerberus.encrypt_message(response.json()['public'], data_to_encrypt)
        print("Encrypted message: ", encrypted_message)

        # Transmit the encrypted data
        response2 = await client.post('http://127.0.0.1:8006/test',
                                      json={"aid": response.json()['aid'], "message": encrypted_message})
        if response2.status_code != 200:
            raise HTTPException(status_code=response2.status_code, detail="Error posting encrypted data")
        print("Response:", response2.json())
        # session = cerberus.get_session(agent_private,)
        server_ecdh = cerberus.decrypt_ecdh_key_with_rsa(agent_rsa_private, response2.json()['encrypted_ecdh'])
        print("server ecdh decoded", server_ecdh)
        server_ecdh2 = load_pem_public_key(server_ecdh.encode('utf-8'))

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

def startServer(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Server started and listening on {ip}:{port}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                uid = conn.recv(4).decode()
                print(f"UID: {uid}")
                
                otp = conn.recv(4).decode()
                print(f"OTP: {otp}")
                if not verifyOTP(otp):
                    print("Invalid OTP.")
                    break
                
                directory = f"./Download/{uid}/"
                os.makedirs(directory, exist_ok=True)
                print(f"Directory {directory} created to store information.")
                
                print(f'Connected by {addr}')
                command = conn.recv(4).decode()
                print(f"Command: {command}")
                
                if command == "SEND":
                    filename_bytes = b''
                    while True:
                        byte = conn.recv(1)
                        if byte == b'\0':
                            break
                        filename_bytes += byte
                    filename = filename_bytes.decode()
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
                    filename_bytes = b''
                    while True:
                        byte = conn.recv(1)
                        if byte == b'\0':
                            break
                        filename_bytes += byte
                    filename = filename_bytes.decode()
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
                
# @app.get("/register/")
# def register(backgroundTasks: BackgroundTasks):
#     ip, port = findOpenPort()
#     # backgroundTasks.add_task(startServer, ip, port)
#     url = "http://127.0.0.1:8000/register/"
#     data = {
#         "ip": ip,
#         "port": port
#     }
#     response = requests.post(url, json=data)
#     print(response.json())
#     return {"ip": ip, "port": port}

@app.get("/startup/")
def startup(backgroundTasks: BackgroundTasks):
    # Verify OTP
    ip, port = findOpenPort()
    backgroundTasks.add_task(startServer, ip, port)
    return {"ip": ip, "port": port}

def verifyOTP(otp):
    otp = "1234"
    if otp == "1234":
        return True