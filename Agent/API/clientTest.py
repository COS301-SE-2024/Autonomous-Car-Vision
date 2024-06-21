import socket
import os
import requests # type: ignore

def send_file(ip, port, filepath):
    filename = os.path.basename(filepath)
    print("File name: ", filename)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        s.sendall(b'UID1')        
        s.sendall(b'1234') 
        s.sendall(b'SEND')
        s.sendall(filename.encode() + b'\0')
        
        with open(filepath, 'rb') as f:
            print(f"Sending file {filename}")
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)
        print(f"File {filename} sent successfully.")
    # socket.close()

def receive_file(ip, port, filename):
    print("File name: ", filename)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        s.sendall(b'UID1')        
        s.sendall(b'1234')
        s.sendall(b'RETR')
        s.sendall(filename.encode() + b'\0')
        
        filepath = "./" + filename
        with open(filepath, 'wb') as f:
            print(f"Receiving file {filename}...")
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"File {filename} received and saved to {filepath}")
    # socket.close()    

if __name__ == "__main__":
    url = "http://localhost:8001/startup/"
    
    # Get IP and Port
    response = requests.get(url)
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
