import socket
import os
import requests # type: ignore
import json

def send_file(ip, port, filepath):
    filename = os.path.basename(filepath)
    print("File name: ", filename)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
         
         # make data above json
        data = {
            'uid': '1234',
            'mid': '5678',
            'size': '1',
            'token': 'HELLO',
            'command': 'SEND'
        }
        
        data = json.dumps(data)
        s.sendall(data.encode() + b'\0')
        s.sendall(filename.encode() + b'\0')
        
        with open(filepath, 'rb') as f:
            print(f"Sending file {filename}")
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)
        print(f"File {filename} sent successfully.")

def receive_file(ip, port, filename):
    print("File name: ", filename)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
       
        # make data above json
        data = {
            'uid': '1234',
            'mid': '5678',
            'size': '1',
            'token': 'HELLO',
            'command': 'RETR'
        }
        
        data = json.dumps(data)
        s.sendall(data.encode() + b'\0')
        filepath = "./" + filename
        s.sendall(filename.encode() + b'\0')
        
        with open(filepath, 'wb') as f:
            print(f"Receiving file {filename}...")
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"File {filename} received and saved to {filepath}")

if __name__ == "__main__":
    url = "http://localhost:8001/startupFTPListener/"
    
    headers = {
    "Content-Type": "application/json",
    }

# Define the body
    body = {
        "uid": "value1\n",
        "mid": "value2\n",
        "size": "HELLO\n",
        "token": "TOEdwadKN\n"
    }
    
    # Get IP and Port
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    ip = data["ip"]
    port = data["port"]
    
    print("IP: ", ip)
    print("Port: ", port)
    
    filepath = "../../Documentation/Images/Donatello.png"
    
    # To send a file
    send_file(ip, port, filepath)
    
    # To receive a file
    # receive_file(ip, port, "Donatello.png")
    
    # move file to new dir
    # os.rename("test.txt", "../../Documentation/Images/Temp/test.txt")
