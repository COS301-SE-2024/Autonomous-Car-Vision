import socket
import os
import json
import sys

def receive_file(ip, port, filename, uid, size, token, mid):
    print("File name: ", filename)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        data = {
            "uid": uid,
            "size": size,
            "token": token,
            "command": "RETR",
            "mid": mid
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
    if len(sys.argv) != 8:
        print("Usage: python script.py <ip> <port> <filepath> <uid> <size> <token> <mid>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]
    uid = sys.argv[4]
    size = sys.argv[5]
    token = sys.argv[6]
    mid = sys.argv[7]
    
    print(f"{ip} {port} {filepath} {uid} {size} {token} {mid}")
    
    receive_file(ip, port, filepath, uid, size, token, mid)
