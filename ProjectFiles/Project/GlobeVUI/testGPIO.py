import os
import RPi.GPIO as GPIO
import time

'''
os.system('aplay ../Media/welcome.wav')
os.system('aplay ../Media/dontgo.wav')
'''

def getDist():
	
	GPIO.output(TRIG, 1)
	GPIO.output(ECHO, 1)

	time.sleep(1)
	GPIO.output(TRIG, 0)
	time.sleep(1)
	GPIO.output(TRIG, 1)
	time.sleep(1)
	GPIO.output(TRIG, 0)
	time.sleep(1)
	GPIO.output(TRIG, 1)
	GPIO.output(ECHO, 0)

	time.sleep(1)
	GPIO.output(TRIG, 0)
	time.sleep(1)
	GPIO.output(TRIG, 1)
	time.sleep(1)
	GPIO.output(TRIG, 0)
	time.sleep(1)
	


GPIO.setmode(GPIO.BOARD)
TRIG = 7
ECHO = 12
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.OUT)

for num in xrange(0, 30):
	 getDist()
GPIO.cleanup()
