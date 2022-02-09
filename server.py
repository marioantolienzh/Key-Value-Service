from socket import *

serverPort = ipp #from ss -t -l on terminal

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((‘’,serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

while True:
  connecitonSocket, addr = serverSocket.accept()
  
sentence = connectionSocket.recv(1024).decode()
capitalizedSentence = sentence.upper() 
connectionSocket.send(capitalizedSentence.encode())
connectionSocket.close()

