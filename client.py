
# from re import I
import socket
import threading 
 
# msgFromClient = "command"

# bytesToSend = str.encode(msgFromClient)

# serverAddressPort   = ("127.0.0.1", 6789)

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


 
# Varför skickas hårdkodat "command" till drönaren? För att gå in i sdk läge? https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)

# msg = "Message from Server {}".format(msgFromServer[0])

# Send to server using created UDP socket

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

# vi hanterar recvfrom i paralella trådar istället
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