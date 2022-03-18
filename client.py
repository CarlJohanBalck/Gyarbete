
from re import I
import socket

 

msgFromClient       = "command"

bytesToSend         = str.encode(msgFromClient)

#serverAddressPort   = ("127.0.0.1", 6789)

serverAddressPort   = ("192.168.10.1", 8889)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
msgFromServer = UDPClientSocket.recvfrom(bufferSize)


msg = "Message from Server {}".format(msgFromServer[0])

# Send to server using created UDP socket

while (True):

    cmd = input()
    if cmd == "quit":
        break

    bytesToSend = str.encode(cmd)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    
    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)

 
response = msgFromServer[0].decode('utf-8')
msg = "Message from Server {}".format(response)

print(msg)