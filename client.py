import socket
import sys
import struct
import time

##
# This code was written by Mario Antolínez Herrera on 22/04/2022
# CSDS 325 TCP-like Protocol over UDP (Project 2)
# Client-Server Paradigm with characters Alice (Client) and Bob (Server)
# THIS IS ALICE'S CODE
# **Note that the Server Code must be executed firstly**
# ***Code uses functions such as "match", which will be only executable with Python Versions newer than Python3.10***
##

#Static Variables
TIMEOUT = 0.5 #in seconds
BUFFERSIZE = 1024
MAX_SEQNUM = 30720

##generatePacket(seqNum, ackNum, window, rest)
#   This function is used to pack the relevant variables to be sent.
#The whole packet has 16 bytes and depending on the value of the flags
#it will take one value or another as showed in the commented tabledef generatePacket(seqNum, ackNum, window, rest):
def generatePacket(seqNum, ackNum, window, rest):
    #rest structure
    #|0|0|0|0|0|0|0|0|0|0|0|0|0|A|S|F|
    #---------------------------------
    #|A|S|F|dec.|
    #|0|0|0| 0  |
    #|0|0|1| 1  |
    #|0|1|0| 2  | SYN
    #|0|1|1| 3  |
    #|1|0|0| 4  | ACK
    #|1|0|1| 5  |
    #|1|1|0| 6  | SYN/ACK
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
#
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

##sendPacket(UDPSocket, packet, serverDirections)
# This function is used to send packets from the UDP Socket connection.
#It sends the packet and informs of the sent packet
##
def sendPacket(UDPSocket, packet, serverDirections, seqNum, rest, lastWasTiemout):
    UDPSocket.sendto(packet, serverDirections)

    if(lastWasTiemout==0):
        lastWasTiemout = ""
    else:
        lastWasTiemout = "(Retransmission) "

    match rest:
        case 2:
            synchronization_notification = "(SYN) "
            acknowledgement_notification = ""
        case 4:
            synchronization_notification = ""
            acknowledgement_notification = "(ACK) "
        case _:
            acknowledgement_notification = ""
            synchronization_notification = ""

    print("Sending packet [" + str(seqNum) + "] " + lastWasTiemout + acknowledgement_notification + synchronization_notification)

##listen(bytesAddressPair, UDPSocket, counter, address, seqNum, ackNum, window, rest)
# This function is used to listen to the UDP Socket the server binded to.
# It also unpacks the data inside the packet calling some of the above declarated
#functions and will output the port of the client who sent the packet to the main program
##
def listen(UDPSocket, seqNum, ackNum, window, rest):
    #initialize local variables
    result_b, result = '', ''

    while(1):
        bytesAddressPair = UDPSocket.recvfrom(BUFFERSIZE)
        if(bytesAddressPair):
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            buffer = struct.unpack('hhhh', message)

            result_b = findValuesAfterCommas(str(buffer), result_b)
            seqNum, ackNum, window, rest = int(result_b[0]), int(result_b[1]), int(result_b[2]), int(result_b[3])
            print("Receiving packet [" + str(seqNum) + "]")

            return seqNum, ackNum, window, rest
            break;

##send_syn() is used to update the values of the packet in case of SYN
def send_syn(seqNum, ackNum, window, rest):
    rest = 2
    return seqNum, ackNum, window, rest

##send_ack() is used to update the values of the packet in case of ACK
def send_ack(seqNum, ackNum, window, rest):
    if(seqNum<=MAX_SEQNUM):
        seqNum = seqNum + 1
    else:
        raise ValueError('Sequence Number Exceeded')
    ackNum = ackNum + 1
    rest = 4
    return seqNum, ackNum, window, rest


##main()
# This is the main program that will run the execution of the UDP SERVER
#If first creates the UDP Server Socket, and then it enters in the section in which
#the connection is stablished and the protocol interaction begins
##
if __name__ == "__main__":
     if len(sys.argv) != 3:
          sys.exit("Usage: python3 client.py [SERVER-HOST-OR-IP] [PORT-NUMBER]")
     serverAddress = sys.argv[1]
     serverPort = int(sys.argv[2])
     serverDirections = (serverAddress, serverPort)

     #init socket
     try:
         UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
         UDPClientSocket.settimeout(TIMEOUT)
         #UDPClientSocket.bind((serverAddress, serverPort))
         print("You have been successfully connected to the UDP Socket.")
     except:
         print("There has been an error while managing your UDP Socket connection...")
         sys.exit(1)

     #packet defined as a struct of bits (represented as integers)
     seqNum, ackNum, window, rest = 0,0,0,0
     #global Global variables
     retransmission, lastWasTiemout = 0,0

     #The connection will be iniciated once the client responds with a 'y'
     answ = input("Hey Alice! Would you like to connect to Bob's server? (y/other to exit connection\n")
     while(True):
         if(retransmission == 0):
             if(answ == 'y'):
                 match seqNum:#THREE-WAY HANDSHAKE PROTOCOL
                    case 0:
                        seqNum, ackNum, window, rest = send_syn(seqNum, ackNum, window, rest)
                        my_packet = generatePacket(seqNum, ackNum, window, rest)
                        sendPacket(UDPClientSocket, my_packet, serverDirections, seqNum, rest, lastWasTiemout)
                        if(lastWasTiemout != 0):
                            lastWasTiemout = 0

                        #wait for the response of the server
                        try:
                            seqNum, ackNum, window, rest = listen(UDPClientSocket, seqNum, ackNum, window, rest)
                        except TimeoutError:
                            print("Timeout Error in " + str(seqNum))
                            retransmission = 1
                            lastWasTiemout = 1
                            pass
                    case 1:

                        #THEORETICAL TIMEOUT AFTER RECEIVING SIN/ACK TO CHECK TIMEOUT BEHAVIOR
                        #print("I am sleeping for 2 seconds...")
                        #time.sleep(3)

                        seqNum, ackNum, window, rest = send_ack(seqNum, ackNum, window, rest)
                        my_packet = generatePacket(seqNum, ackNum, window, rest)
                        sendPacket(UDPClientSocket, my_packet, serverDirections, seqNum, rest, lastWasTiemout)
                        if(lastWasTiemout != 0):
                            lastWasTiemout = 0
                        #DO NOT WAIT FOR RESPONSE OF SERVER, JUST ACK THE SYN/ACK
                    case _:
                        print("Connection to Bob's Server Succesfully Done")
                        sys.exit(1)
                        #THIS WOULD BE THE BEHAVIOR OF THE PROTOCOL AFTER HANDSHAKE
                        pass
             else:
                 print("Ending Connection Establishment...")
                 sys.exit(1)
         else:
             retransmission = 0
             print("Retransmitting packet " + str(seqNum))
