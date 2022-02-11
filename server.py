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
        out=1
        while out!=0:
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

                        if(msg=='help'):
                            conn.sendall(b'help/get key/put key value/values/keyset/mapping/bye ')
                        if(msg[0:3]=='get'):
                            print('check1')
                            value=df["key"].iloc[0]
                            key = msg[4:(len(msg)-1)]
                            display(df)
                            conn.sendall(bytes(row_1, 'utf-8'))#NEED TO GET THE value for the KEY
                            pass
                        if(msg[0:3]=='put'):
                            first_gap_pos = msg.find(" ")
                            second_gap_pos = (msg.find(" "), first_gap_pos+1)
                            key = msg[4:first_gap_pos]
                            print(key)
                            value = msg[(second_gap_pos+1):(len(msg)-1)]
                            print(value)
                            df.loc[len(df.index)] = [key, value]
                            display(df)
                            conn.sendall(b'new df')
                            print('check2')
                            pass
                        if(msg[0:3]=='values'):
                            print('check3')
                            pass
                        if(msg[0:3]=='keyset'):
                            print('check4')
                            pass
                        if(msg[0:3]=='mappings'):
                            print('check5')
                            pass
                        if(msg[0:3]=='bye'):
                            out=0
                            break

            else:
                print('Ending connection')
                break
