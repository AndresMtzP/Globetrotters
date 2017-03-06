import pyautogui
from multiprocessing import Process

def main():
	# will print screen size of the current computer
	getScreenSize()
	# moves mouse to these x-y pixel coordinates for the specified duration
	# using pyautogui functions
	for i in range(3):
		pyautogui.moveTo(0, 100, duration=2)
		pyautogui.moveTo(100, 100, duration=1)
	print "End main\n"

def getScreenSize():
	print str(pyautogui.size())
	
def testFun():
	# simple counter used to test the execution of multiprocessing functions
	count = 0;
	while count < 1000:
		print str(count) + '\n'
		count = count + 1
	print "End testFun"
	
if __name__ == '__main__':
	# assign processes and execute them in parallel
	p1 = Process(target = main)
	p1.start()
	p2 = Process(target = testFun)
	p2.start()
