import sys
import socket
import time

MSG_RECEIVED = 1

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

HOST = input('Enter the IP address or Hostname of the server: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Please wait while I connect you...') #TIMEOUT??
    s.sendall(b'Hello, this is the client')

    interactions_expected = 3
    interactions = 0

    while(interactions<interactions_expected):
        data1 = s.recv(1024)
        if(interactions<2):
            byt = bytes(str(interactions), 'utf-8')
            print('Received', repr(data1), '\n')
            s.sendall(bytes('received #', 'utf-8') + byt)
            interactions+=1
        if(interactions==2):
            while True:
                to_send = input('_: ')
                s.sendall(bytes(to_send, 'utf-8'))
                time.sleep(1)#waiting for cmd response
                data3 = s.recv(1024)#PONER UN TIMEOUT=> ERR
                print(repr(data3))



    print('\n Closing socket connection...')
