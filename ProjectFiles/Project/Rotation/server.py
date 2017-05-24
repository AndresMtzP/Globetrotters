#!/usr/bin/python
import socket
import sys
import os
        
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
print("Globe Cntrl Server IP: ")
#serverIP = str(os.system("curl -s https://api.ipify.org"))
serverIP = "146.244.121.186"
server_address = (serverIP, 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            data = connection.recv(16)
            print >> sys.stderr, 'received "%s"' % data
            if data:
                with open('/home/pi/globe/Rotation/commands', 'w') as f:
                    f.write(data)     
            else:
                break
    finally:
        connection.close()