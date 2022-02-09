
import socket

serverName = '192.168.1.87'  # Standard loopback interface address (localhost)
serverPort = 65432

print('Welcome to the keyValue Service Client\n')
token = 0

while(token == 0):
    serverName = raw_input('Enter the IP address of Hostname of the server: ')
    serverPort = raw_input('Enter the port of the server: ')
    try:
        print('Please wait while I connect you...\n')
        
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        sentence = raw_input(‘Input lowercase sentence:’)
        
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(1024)
        print (‘From Server:’, modifiedSentence.decode())
        
        clientSocket.close()
        token = 1
        break
    except ValueError:
        print("Oops!  There was some error when connecting to the server. Please try again...\n")
