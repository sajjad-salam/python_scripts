# python tcp server and udp
# this is server tcp 
import socket
serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostbyname()
port = 444
serversocket.bind((host,port))
serversocket.listen(3)
while True :
    clientsocket,adress=serversocket.accept()
    print("reseve connection from " % str(adress))
    message='hellllllo ! thank you for connetion'+"\r\n"
    clientsocket.send(message)
    clientsocket.close()