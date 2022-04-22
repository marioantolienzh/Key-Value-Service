import socket
import sys
import struct
import time

##
# This code was written by Mario Antolínez Herrera on 22/04/2022
# CSDS 325 TCP-like Protocol over UDP (Project 2)
# Client-Server Paradigm with characters Alice (Client) and Bob (Server)
# THIS IS BOB'S CODE
##

#Static variables
TIMEOUT = 0.5 #in seconds
BUFFERSIZE = 1024
MAX_SEQNUM = 30720

##generatePacket(seqNum, ackNum, window, rest)
# This function is used to pack the relevant variables to be sent.
# The whole packet has 16 bytes and depending on the value of the flags
#it will take one value or another as showed in the commented table
##
def generatePacket(seqNum, ackNum, window, rest):
    #rest structure
    #|0|0|0|0|0|0|0|0|0|0|0|0|0|A|S|F|
    #---------------------------------
    #|A|S|F|dec.|
    #|0|0|0| 0  |
    #|0|0|1| 1  |
    #|0|1|0| 2  |
    #|0|1|1| 3  |
    #|1|0|0| 4  |
    #|1|0|1| 5  |
    #|1|1|0| 6  |
    #|1|1|1| 7  |
    #----------------------------------
    packet = struct.pack('hhhh',
            seqNum,          #seqNum
            ackNum,          #ackNum
            window,          #window size
            rest             #16bits that have to be specified
    )
    return packet

##findValuesAfterCommas(buffer, result_b)
# This function is used to extract the data from the raw packet stored in buffer
#and will store the output result in result_b.
##
def findValuesAfterCommas(buffer, result_b):
    #init local variables
    counter = 0

    for i in range(1, len(buffer)):
        if(buffer[i] == ','):
            result_b += buffer[i-1]#MIGHT GO FARTHER THAN LENGTH, PUT A WHILE
            counter = counter + 1
        if(buffer[i] == ')'):
            result_b += buffer[i-1]#MIGHT GO FARTHER THAN LENGTH, PUT A WHILE
            counter = counter + 1
    return result_b

##findPortInAddress(address, result_a)
# This function is used to extract the data of the client port from the encoded
#data in address. We will suppose the port # will have 5 digits
##
def findPortInAddress(address, result_a):
    for i in range(0, len(address)):
        if(address[i] == ','):
            try:
                result_a += address[i + 2]
                result_a += address[i + 3]
                result_a += address[i + 4]
                result_a += address[i + 5]
                result_a += address[i + 6]
            except:
                print("ArrayIndexOutOfBounds Error.")
    return result_a

##init(UDPSocket, port)
# This function is used to init the UDP Socket, it takes as input a UDPSocket
#object and the port number which it will bind to and listen
##
def init(UDPSocket, port):
    UDPSocket.bind(('', port))
    print("UDP server up and listening...")

##listen(UDPSocket, counter, address, seqNum, ackNum, window, rest)
# This function is used to listen to the UDP Socket the server binded to.
#It also unpacks the data inside the packet calling some of the above declarated
#functions and will output the port of the client who sent the packet to the main program
##
def listen(UDPSocket, seqNum, ackNum, window, rest):
    #local variables declaration
    result_a, result_b, address = '', '', ''
    #variable that counts the interations with the server

    while(1):
        bytesAddressPair = UDPSocket.recvfrom(BUFFERSIZE)
        if(bytesAddressPair):
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            clientPort = findPortInAddress(str(address), result_a)
            buffer = struct.unpack('hhhh', message)

            result_b = findValuesAfterCommas(str(buffer), result_b)
            seqNum, ackNum, window, rest = int(result_b[0]), int(result_b[1]), int(result_b[2]), int(result_b[3])
            print("Receiving packet [" + str(seqNum) + "]")

            #GET THE VALUES OF FLAGS FROM THE message...[seqNum, ackNum, window, rest] = 0,0,0,0
            return int(clientPort) , seqNum, ackNum, window, rest
            break;

##sendPacket(UDPSocket, packet, serverDirections, seqNum, rest, lastWasTiemout)
# This function is used to send packets from the UDP Socket connection.
#It sends the packet and informs of the sent packet.
##
def sendPacket(UDPSocket, packet, serverDirections, seqNum, rest, lastWasTiemout):
    UDPSocket.sendto(packet, serverDirections)

    if(lastWasTiemout==0):
        lastWasTiemout = ""
    else:
        lastWasTiemout = "(Retransmission) "

    match rest:
        case 6:
            synack_notification = "(SYN/ACK) "
        case _:
            synack_notification = ""

    print("Sending packet [" + str(seqNum) + "] " + lastWasTiemout + synack_notification)

##main()
# This is the main program that will run the execution of the UDP SERVER CONNECTION
#If first creates the UDP Server Socket, and then it enters in the section in which
#the connection is stablished following the 3-Way-Handshake
# **Note that the Server Code must be executed firstly**
# ***Code uses functions such as "match", which will be only executable with Python Versions newer than Python3.10***

##
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 server.py [PORT-NUMBER]")
    serverPort = int(sys.argv[1])

    #initiating Global variables
    interactions, retransmission, endOfHandshake, lastWasTiemout = 0,0,0,0
    seqNum, ackNum, window, rest = 0,0,0,0

    #init socket
    try:
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        init(UDPServerSocket, serverPort)
    except:
        print("There has been an error while managing your UDP connection...")
        sys.exit(1)


    while(True):
        #CONNECTION STABLISHEMENT COMMUNICATION
        if(retransmission == 0):
                #set timeout after first arrival of packet
                if(interactions == 1):
                    UDPServerSocket.settimeout(TIMEOUT)
                else:
                    pass

                #send packet when received, and change the parameters of the package depending on the received values
                try:
                    clientPort, seqNum, ackNum, window, rest = listen(UDPServerSocket, seqNum, ackNum, window, rest)
                    interactions = interactions + 1
                except TimeoutError:
                    print("Timeout Error in " + str(seqNum))
                    retransmission = 1
                    lastWasTiemout = 1
                    pass
                #WILL ONLY CONSIDER TWO CASES: SYN AND ACK
                match rest:
                    case 2:
                        seqNum = seqNum + 1
                        rest = 6
                    case 4:
                        seqNum = seqNum + 1
                        rest = 0
                        endOfHandshake = 1
                        #PROGRAM WOULD STOP HERE
                    case _:
                        #THIS WOULD BE OTHER CASES NOT CONSIDERED IN THIS SIMPLE EXECUTION
                        pass
                if(endOfHandshake == 1):
                    print("Connection to Alice Succesfully Done")
                    sys.exit(1)

                #THEORETICAL TIMEOUT AFTER RECEIVING SYN TO CHECK TIMEOUT BEHAVIOR
                #print("I am sleeping for 2 seconds...")
                #time.sleep(2)

                syn_packet = generatePacket(seqNum, ackNum, window, rest)
                sendPacket(UDPServerSocket, syn_packet, ('', clientPort), seqNum, rest, lastWasTiemout)
                if(lastWasTiemout != 0):
                    lastWasTiemout = 0
        else:
            retransmission = 0
            print("Retransmitting packet " + str(seqNum))

