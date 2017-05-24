import os
import RPi.GPIO as GPIO
import time
from random import randint
import json
import multiprocessing
import os.path


seqNum = [0]
voice = False


def userDist():
	# Config GPIO to ID pins by layout
	# Ultrasonic Echo output feeds into voltage divider to drop 5v ~= 3.3v
	# RPi reads Echo value between 1K Ohm & 2k Ohm resistors. 2k connects to GND
	GPIO.setmode(GPIO.BOARD)
	TRIG = 8
	ECHO = 10
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.output(TRIG, 0)
	GPIO.setup(ECHO, GPIO.IN)
	#Min delay after pin setup
	time.sleep(0.1)
	
	GPIO.output(TRIG, 1)
	time.sleep(0.0001)
	GPIO.output(TRIG, 0)

	# Detect rising edge of echo signal
	while(GPIO.input(ECHO) == 0):
		pass
	start = time.time()
	# Detect falling edge of echo signal
	while(GPIO.input(ECHO) == 1):
		pass
	stop = time.time()

	# Speed of sound = 340 m/s. R = D/T
	# Solve for distance (D) and divide in half to get
	# distance traveled in one direction before boucing back
	dist = ((stop - start) * 170)
	# print the user's distance away from Trotter in meters
	#print("userDist: {}".format(dist))
	#GPIO.cleanup()
	return(dist)
	


def userDetect():
	print("User Detection enabled")
	activeUser = 'no'
	while True:
		time.sleep(1)
		# Detect user within 1 meter of Trotter
		if(userDist() < 1 and activeUser == 'no'):
		 	time.sleep(3)
		 	if(userDist() < 1 and activeUser == 'no'):
		 		print("UserDetect: User detected")
		 		activeUser = 'yes'
    			GUICom2("welcome")
    			if(voice == True):
    				os.system('aplay /home/pi/globe/Media/welcome.wav')
    			GUICom2("map")
		 # Detect if user has departed
		elif(userDist() > 2 and activeUser == 'yes'):
	 		#time.sleep(0.5)
	 		if(userDist() > 2 and activeUser == 'yes'):
	 			print("UserDetect: User departed")
	 			randNum = randint(0,2)
	 			if(randNum == 2):
					GUICom2("arnold")
				else:
					GUICom2("goodbye")
				if(voice == True):
			 		# Plays random departure msg.  0-dontgo  1-comeback  2-arnold
					os.system("aplay /home/pi/globe/Media/depart{}.wav".format(randNum))
		 		activeUser = 'no'
		 		GUICom2("map")
	 	# Testing
	 	#print("{} {}".format(userDist(), activeUser))


def GUICom2(GUICmd):
	# Commands: welcome, goodbye, map
	seqNum[0] = ((seqNum[0] + 1) % 3) + 6
	print("GUICom2: {}. Sequence# {}".format(GUICmd, seqNum[0]))
	# Create JSON file to comm with HTML GUI
	data = {"GUICommand" : GUICmd, "SeqNum" : seqNum[0]}
	with open('/var/www/html/GUICom.json', 'w') as outfile:
		json.dump(data, outfile)




userDetect()





