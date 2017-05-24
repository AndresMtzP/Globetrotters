
from teleportapi import *
import multiprocessing
import os.path
import sys
import json



def getInfo(loc):
	
	print("getInfo: looking up {}".format(loc))

	
	locName = getFullName(loc)
	print("getInfo: locName returned {}".format(locName))
	if(locName == None):
		return("None")
	
	# Rotate globe to longitude
	# globeCntrl(str(locLon))
	# construct output for Alexa. Comm with API & MySQL database
	locList = getAll(loc)

	# Create new process to updates data and Images for GUI 
	if locList:
		GUIProc = multiprocessing.Process(target=GUI, args=(locList[0]['Name'],))
		GUIProc.start()

	return locList
	




def moreInfo(loc):
	print("details: {}".format(loc))
	return("More details to come soon for {}".format(loc))




def GUI(location):
	getImage(location)



def GUICom(GUICmd, seqNum):
	# Commands: switchView, help, welcome, goodbye, defaultZoom
	# zoomIn, zoomOut, globetrotters, details, map, about
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
	with open('../Rotation/commands', 'w') as f:
    		f.write(command)
	



























