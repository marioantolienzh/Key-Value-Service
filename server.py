import sys
import socket
import time
import pandas as pd
from IPython.display import display

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

df = pd.DataFrame({
    "Key": ['Key'],
    "Value": [0]
})

display(df)

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
                if(counter==2):
                    while True:
                        time.sleep(1)
                        data2 = conn.recv(1024)
                        msg = data2.decode("utf-8")
                        print(msg)
                        print(msg[0:2])
                        if(msg=='help'):
                            conn.sendall(b'help/get key/put key value/values/keyset/mapping/bye ')
                        if(msg=='get key'):
                            print('check1')
                            pass
                        if(msg[0:3]=='put'):
                            conn.sendall(b'whatuver')
                            gap_pos = data2.decode("utf-8").find(" ")
                            print(gap_pos)
                            #df.loc[len(df.index)] = [index, 'whatever']
                            display(df)
                            print('check2')
                            pass
                        if((data2.decode("utf-8"))=='values'):
                            print('check3')
                            pass
                        if((data2.decode("utf-8"))=='keyset'):
                            print('check4')
                            pass
                        if((data2.decode("utf-8"))=='mappings'):
                            print('check5')
                            pass
                        if((data.decode("utf-8"))=='bye'):
                            print('check6')
                            break

            else:
                print('Ending connection')
                break
