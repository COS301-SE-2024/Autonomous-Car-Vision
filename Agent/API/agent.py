from fastapi import FastAPI, BackgroundTasks
import socket
import os
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

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
                mid = conn.recv(4).decode()
                mname = conn.recv(4).decode()
                print(f"UID: {uid}, MID: {mid}, MNAME: {mname}")
                
                otp = conn.recv(4).decode()
                print(f"OTP: {otp}")
                if not verifyOTP(otp):
                    print("Invalid OTP.")
                    break
                
                directory = f"./serverData/{uid}/"
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
                
@app.get("/register/")
def register(backgroundTasks: BackgroundTasks):
    ip, port = findOpenPort()
    # backgroundTasks.add_task(startServer, ip, port)
    url = "http://127.0.0.1:8000/register/"
    data = {
        "ip": ip,
        "port": port
    }
    response = requests.post(url, json=data)
    print(response.json())
    return {"ip": ip, "port": port}
    

@app.get("/startup/")
def startup(backgroundTasks: BackgroundTasks):
    # Verify OTP
    ip, port = findOpenPort()
    backgroundTasks.add_task(startServer, ip, port)
    return {"ip": ip, "port": port}

def verifyOTP():
    otp = "1234"
    if otp == "1234":
        return True