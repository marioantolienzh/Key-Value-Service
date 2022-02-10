import sys
import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        counter = 0
        while True:
            data = conn.recv(1024)
            print(data)
            if data:
                if(counter==0):
                    conn.sendall(b'Welcome to the keyValue Service')
                    counter+=1
                if(counter==1):
                    time.sleep(1)
                    conn.sendall(b'KeyValue Service> ')
                    counter+=1
            else:
                print('Ending connection')
                break
