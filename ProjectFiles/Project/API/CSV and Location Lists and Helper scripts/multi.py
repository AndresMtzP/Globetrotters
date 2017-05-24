import thread
import time

def getAll():
	print 'Retrieving Values for location'

def getSpeech(loc, map):
	print 'Alexa reading information about %s' % loc
	time.sleep(10)
	print 'Alexa done reading'

def getImage(loc, maps):
	print 'Getting image from server'
	time.sleep(5)
	print 'Done getting images'
	print maps

getAll()

try:
	thread.start_new_thread(getSpeech, ("loc", 1))
	thread.start_new_thread(getImage, ("loc", 1))
except:
	print "Unable to start thread"

while 1:
	pass