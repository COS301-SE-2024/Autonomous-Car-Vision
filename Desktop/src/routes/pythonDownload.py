import socket
import os
import json
import sys

def send_file(ip, port, filepath, uid, size, token):
    filename = os.path.basename(filepath)
    print("File name: ", filename)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        data = {
            "uid": uid,
            "size": size,
            "token": token,
            "command": "SEND",
        }

        data = json.dumps(data)
        s.sendall(data.encode() + b"\0")
        s.sendall(filename.encode() + b"\0")

        with open(filepath, "rb") as f:
            print(f"Sending file {filename}")
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)
        print(f"File {filename} sent successfully.")

def receive_file(ip, port, filename, uid, size, token):
    print("File name: ", filename)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        data = {
            "uid": uid,
            "size": size,
            "token": token,
            "command": "RETR",
        }

        data = json.dumps(data)
        s.sendall(data.encode() + b"\0")
        filepath = "./" + filename
        s.sendall(filename.encode() + b"\0")

        with open(filepath, "wb") as f:
            print(f"Receiving file {filename}...")
            while True:
                data = s.recv(1024)
                if not data:
                    break;
                f.write(data)
        print(f"File {filename} received and saved to {filepath}")


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python script.py <ip> <port> <filepath> <uid> <size> <token>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]
    uid = sys.argv[4]
    size = sys.argv[5]
    token = sys.argv[6]
    
    print(f"{ip} {port} {filepath} {uid} {size} {token}")
    
    receive_file(ip, port, filepath, uid, size, token)
