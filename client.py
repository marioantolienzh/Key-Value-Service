
import socket

serverName = '192.168.1.87'  # Standard loopback interface address (localhost)
serverPort = 65432

print('Welcome to the keyValue Service Client\n')
token = 0

while(token == 0):
    inp = input('Enter the IP address of Hostname of the server: ')

    try:
        print('Please wait while I connect you...\n')
        token = 1
        break
    except ValueError:
        print("Oops!  There was some error when connecting to the server. Please try again...\n")
