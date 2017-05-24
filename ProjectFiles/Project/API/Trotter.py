
from teleportapi import *
import multiprocessing
import os.path
import sys
import json



def moreInfo(loc):
	print("details: {}".format(loc))
	return("More details to come soon for {}".format(loc))



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
	# code to control the rotation and speed of the globe Comm with PIC uC
	print("globeCntrl: {}".format(command))
	with open('/home/pi/globe/Rotation/commands', 'w') as f:
    		f.write(command)
	



























