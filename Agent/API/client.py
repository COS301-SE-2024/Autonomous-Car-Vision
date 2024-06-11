import socket
import os

def send_file(ip, port, filepath):
    filename = os.path.basename(filepath)
    print("File name: ", filename)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(b'SEND')
        s.sendall(filename.encode() + b'\0')  # Send filename followed by a null byte
        
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
        s.sendall(b'RETR')
        s.sendall(filename.encode() + b'\0')  # Send filename followed by a null byte
        
        filepath = "./" + filename
        with open(filepath, 'wb') as f:
            print(f"Receiving file {filename}...")
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"File {filename} received and saved to {filepath}")

if __name__ == "__main__":
    ip = "10.32.130.218"
    port = 8001
    filepath = "../../Documentation/Images/Temp/video.mp4"
    
    # To send a file
    send_file(ip, port, filepath)
    
    # To receive a file
    receive_file(ip, port, "test.txt")
    
    # move file to new dir
    os.rename("test.txt", "../../Documentation/Images/Temp/test.txt")
