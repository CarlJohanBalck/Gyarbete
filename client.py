
# from re import I
import socket
import threading 
 
# varför ett hårdkodat "command"?
# msgFromClient = "command"

# bytesToSend = str.encode(msgFromClient)

#serverAddressPort   = ("127.0.0.1", 6789)

serverAddressPort = ("192.168.10.1", 8889)

bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def recv():
    count = 0
    while True: 
        try:
            data, server = UDPClientSocket.recvfrom(bufferSize)
            print("Message from Server {}", data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


 
# Varför skickas hårdkodat "command" till drönaren utanför while-loopen? 
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# client.py går inte vidare efter denna linje, utan försöker att lyssna på servern. Vi når aldrig while-true loopen.
# msgFromServer = UDPClientSocket.recvfrom(bufferSize)

# 
# msg = "Message from Server {}".format(msgFromServer[0])

# Send to server using created UDP socket
# Nice to have: påminna om de kommandon man kan använda


print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

while True:
    try:
        cmd = input("")

        if not cmd: 
            break

        if 'quit' in cmd:
            print ('...')
            UDPClientSocket.close()  ## Stäng socket när vi avslutar 
            break
        bytesToSend = str.encode(cmd)
        sent = UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        # vi hanterar recvfrom i paralella trådar istället
        # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        
        # msg = "Message from Server {}".format(msgFromServer[0])

    except KeyboardInterrupt:
            print ('\n . . .\n')
            UDPClientSocket.close()  
            break

# anledning utanför while-loop?
# response = msgFromServer[0].decode('utf-8')
# msg = "Message from Server {}".format(response)

#print(msg)