import sys
import socket
import time

MSG_RECEIVED = 1

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

HOST = input('Enter the IP address or Hostname of the server: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Please wait while I connect you...')
    s.sendall(b'Hello, this is the client')

    interactions_expected = 3
    interactions = 0

    while(interactions<interactions_expected):
        data1 = s.recv(1024)
        if(interactions<interactions_expected-1):
            interactions+=1
            byt = bytes(str(interactions), 'utf-8')
            print('Received', repr(data1), '\n')
            s.sendall(b'received #' + byt)
        else:
            to_send = input('_:')
            s.sendall(b'' + bytes(to_send))
    print('\n Closing socket connection...')
