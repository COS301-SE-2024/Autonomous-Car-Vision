from fastapi import FastAPI, BackgroundTasks
import socket
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

def findOpenPort():
    port = 8001
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
    directory = f"./serverData"
    os.makedirs(directory, exist_ok=True)
    print(f"Directory {directory} created to store information.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Server started and listening on {ip}:{port}")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                with open(os.path.join(directory, "receivedData.txt"), "ab") as f:
                    f.write(data)
                conn.sendall(data)
                
@app.get("/register/")
def register(backgroundTasks: BackgroundTasks):
    ip, port = findOpenPort()
    backgroundTasks.add_task(startServer, ip, port)
    return {"ip": ip, "port": port}

@app.get("/startup/")
def startup(backgroundTasks: BackgroundTasks):
    ip, port = findOpenPort()
    backgroundTasks.add_task(startServer, ip, port)
    return {"ip": ip, "port": port}