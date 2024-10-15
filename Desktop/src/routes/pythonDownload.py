import socket
import os
import json
import sys

def receive_file(ip, port, filename, fullFilepath, uid, size, token, mid, videoDestination):
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

        print("BEFORE RECEIVE")
        with open(filepath, "wb") as f:
            print(f"Receiving file {filename}...")
            while True:
                data = s.recv(1024)
                if not data:
                    break;
                f.write(data)
        print(f"File {filename} received and saved to {filepath}")
        
        print("AFTER RECEIVE")
        # move the file to the videoDestination
        os.rename(fullFilepath, videoDestination)


if __name__ == "__main__":
    if len(sys.argv) != 10:
        print("Usage: python script.py <ip> <port> <filepath> <fullFilepath> <uid> <size> <token> <mid>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]
    fullFilepath = sys.argv[4]
    uid = sys.argv[5]
    size = sys.argv[6]
    token = sys.argv[7]
    mid = sys.argv[8]
    videoDestination = sys.argv[9]
    
    print(f"{ip} {port} {filepath} {fullFilepath} {uid} {size} {token} {mid} {videoDestination}")
    
    receive_file(ip, port, filepath, fullFilepath, uid, size, token, mid, videoDestination)

