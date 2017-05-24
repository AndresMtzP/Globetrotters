
from teleportapi import *
import multiprocessing
import os.path
import sys
import socket
import json



def GUI(GUICmd, seqNum, fullName):
	GUIProc = multiprocessing.Process(target=updateGUI, args=(GUICmd, seqNum, fullName,))
	GUIProc.start()



def updateGUI(GUICmd, seqNum, fullName):
	getImage(fullName)
	GUICom(GUICmd, seqNum)



def GUICom(GUICmd, seqNum):
	# Commands: switchView, help, welcome, goodbye, defaultZoom
	# zoomIn, zoomOut, globetrotters, details, map, about, Option{}
	if(GUICmd == "in"):
		GUICmd = "zoomIn"
	elif(GUICmd == "out"):
		GUICmd = "zoomOut"
	elif(GUICmd == "reset"):
		GUICmd = "defaultZoom"

	print("GUICom: {}. Sequence# {}".format(GUICmd, seqNum))
	# Create JSON file to comm with HTML GUI
	data = {"GUICommand" : GUICmd, "SeqNum" : seqNum}
	with open('/var/www/html/GUICom.json', 'w') as outfile:
		json.dump(data, outfile)



def globeCntrl(command):
	# Tx command to remote globe controller
	globeCntrlRemote(command)
	# code to control the rotation and speed of the globe Comm with PIC uC
	print("globeCntrl: {}".format(command))
	with open('/home/pi/globe/Rotation/commands', 'w') as f:
    		f.write(command)
	


def globeCntrlRemote(command):
	serverIP = '146.244.121.186'
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port on the server given by the caller
    server_address = (serverIP, 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        
        message = command
        print >> sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print >>sys.stderr, 'received "%s"' % data

    finally:
        sock.close()
























